param([Parameter(Mandatory=$true)][string]$Request, [switch]$JoinJob)
$ErrorActionPreference = 'Stop'
$config = Get-Content -LiteralPath $Request -Raw | ConvertFrom-Json

# This is the Windows OS adapter, not a PID-tree discovery heuristic. The Job
# disallows breakaway and remains owned outside the command's process tree.
Add-Type -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Runtime.InteropServices;
public static class ConsumerJob {
    [StructLayout(LayoutKind.Sequential)] struct BasicLimits {
        public long ProcessTime, JobTime;
        public uint Flags;
        public UIntPtr MinimumWorkingSet, MaximumWorkingSet;
        public uint ActiveProcessLimit;
        public UIntPtr Affinity;
        public uint PriorityClass, SchedulingClass;
    }
    [StructLayout(LayoutKind.Sequential)] struct ExtendedLimits {
        public BasicLimits Basic;
        public ulong ReadOperations, WriteOperations, OtherOperations, ReadBytes, WriteBytes, OtherBytes;
        public UIntPtr ProcessMemory, JobMemory, PeakProcessMemory, PeakJobMemory;
    }
    [StructLayout(LayoutKind.Sequential)] struct Accounting {
        public long UserTime, KernelTime, PeriodUserTime, PeriodKernelTime;
        public uint PageFaults, TotalProcesses, ActiveProcesses, TerminatedProcesses;
    }
    [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
    static extern IntPtr CreateJobObject(IntPtr attributes, string name);
    [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
    static extern IntPtr OpenJobObject(uint access, bool inherit, string name);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool SetInformationJobObject(IntPtr job, int kind, ref ExtendedLimits limits, uint size);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool QueryInformationJobObject(IntPtr job, int kind, out Accounting info, uint size, IntPtr returned);
    [DllImport("kernel32.dll", EntryPoint="QueryInformationJobObject", SetLastError=true)]
    static extern bool QueryProcessIds(IntPtr job, int kind, IntPtr info, uint size, IntPtr returned);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern IntPtr OpenProcess(uint access, bool inherit, uint pid);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool IsProcessInJob(IntPtr process, IntPtr job, out bool belongs);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern uint WaitForSingleObject(IntPtr handle, uint milliseconds);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool AssignProcessToJobObject(IntPtr job, IntPtr process);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool TerminateJobObject(IntPtr job, uint code);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool CloseHandle(IntPtr handle);
    static void Check(bool success) { if (!success) throw new Win32Exception(Marshal.GetLastWin32Error()); }
    public static IntPtr Create(string name) {
        IntPtr job = CreateJobObject(IntPtr.Zero, name);
        Check(job != IntPtr.Zero);
        try {
            ExtendedLimits limits = new ExtendedLimits();
            limits.Basic.Flags = 0x2000; // JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE; no breakaway.
            Check(SetInformationJobObject(job, 9, ref limits, (uint)Marshal.SizeOf(limits)));
            return job;
        } catch { CloseHandle(job); throw; }
    }
    public static void Join(string name) {
        IntPtr job = OpenJobObject(1, false, name); // JOB_OBJECT_ASSIGN_PROCESS
        Check(job != IntPtr.Zero);
        try { Check(AssignProcessToJobObject(job, new IntPtr(-1))); }
        finally { CloseHandle(job); }
    }
    public static uint Active(IntPtr job) {
        Accounting info;
        Check(QueryInformationJobObject(job, 1, out info, (uint)Marshal.SizeOf(typeof(Accounting)), IntPtr.Zero));
        return info.ActiveProcesses;
    }
    static uint[] ProcessIds(IntPtr job, DateTime deadline) {
        uint capacity = Math.Max(Active(job), 1u);
        while (DateTime.UtcNow < deadline) {
            // JOBOBJECT_BASIC_PROCESS_ID_LIST: two DWORDs followed by ULONG_PTRs.
            int size = checked(8 + checked((int)capacity) * IntPtr.Size);
            IntPtr buffer = Marshal.AllocHGlobal(size);
            try {
                Marshal.WriteInt32(buffer, 0, 0);
                Marshal.WriteInt32(buffer, 4, 0);
                bool success = QueryProcessIds(job, 3, buffer, (uint)size, IntPtr.Zero);
                int error = success ? 0 : Marshal.GetLastWin32Error();
                if (!success && error != 234) throw new Win32Exception(error); // ERROR_MORE_DATA
                uint assigned = (uint)Marshal.ReadInt32(buffer, 0);
                uint listed = (uint)Marshal.ReadInt32(buffer, 4);
                if (!success || listed < assigned) {
                    capacity = Math.Max(assigned, checked(capacity * 2));
                    continue;
                }
                if (listed > capacity) throw new InvalidOperationException("Invalid Windows Job process list");
                uint[] ids = new uint[listed];
                for (int index = 0; index < ids.Length; index++)
                    ids[index] = checked((uint)Marshal.ReadIntPtr(buffer, 8 + index * IntPtr.Size).ToInt64());
                return ids;
            } finally { Marshal.FreeHGlobal(buffer); }
        }
        throw new TimeoutException("Windows Job membership unconfirmed");
    }
    public static bool Shutdown(IntPtr job, DateTime deadline, bool interrupted) {
        ExtendedLimits limits = new ExtendedLimits();
        limits.Basic.Flags = 0x2008; // KILL_ON_JOB_CLOSE | ACTIVE_PROCESS; no breakaway.
        limits.Basic.ActiveProcessLimit = 0;
        if (!SetInformationJobObject(job, 9, ref limits, (uint)Marshal.SizeOf(limits)))
            throw new Win32Exception(Marshal.GetLastWin32Error(), "Windows Job ActiveProcessLimit=0 rejected");
        Console.Error.WriteLine("{\"windows_job_admission_limit\":0,\"accepted\":true}");
        uint[] ids = ProcessIds(job, deadline);
        Console.Error.WriteLine("{\"windows_job_shutdown_snapshot\":[" + String.Join(",", ids) + "]}");
        var processes = new List<IntPtr>();
        try {
            bool live = false;
            foreach (uint pid in ids) {
                if (DateTime.UtcNow >= deadline) throw new TimeoutException("Windows Job membership unconfirmed");
                IntPtr process = OpenProcess(0x101000, false, pid); // SYNCHRONIZE | QUERY_LIMITED_INFORMATION
                if (process == IntPtr.Zero) {
                    int error = Marshal.GetLastWin32Error();
                    if (error == 87) continue; // PID already freed (ERROR_INVALID_PARAMETER).
                    throw new Win32Exception(error);
                }
                processes.Add(process);
                bool belongs;
                Check(IsProcessInJob(process, job, out belongs));
                if (!belongs) {
                    // Association cannot be broken: this numeric PID was recycled.
                    processes.RemoveAt(processes.Count - 1);
                    Check(CloseHandle(process));
                    continue;
                }
                uint state = WaitForSingleObject(process, 0);
                if (state == 258) live = true; // WAIT_TIMEOUT: still nonsignaled.
                else if (state == 0xffffffff) throw new Win32Exception(Marshal.GetLastWin32Error());
                else if (state != 0) throw new InvalidOperationException("Windows Job process wait unconfirmed");
            }
            bool orphan = !interrupted && Active(job) > 0 && live;
            // Accounting zero can precede cwd-handle rundown; retain handles across termination.
            if (interrupted || orphan) Check(TerminateJobObject(job, 1));
            foreach (IntPtr process in processes) {
                uint remaining = (uint)Math.Max(0, Math.Ceiling((deadline - DateTime.UtcNow).TotalMilliseconds));
                uint state = WaitForSingleObject(process, remaining);
                if (state == 258) throw new TimeoutException("Windows Job shutdown unconfirmed");
                if (state == 0xffffffff) throw new Win32Exception(Marshal.GetLastWin32Error());
                if (state != 0) throw new InvalidOperationException("Windows Job process wait unconfirmed");
            }
            return orphan;
        } finally {
            foreach (IntPtr process in processes) Check(CloseHandle(process));
        }
    }
}
'@

if ($JoinJob) {
    # Assignment occurs before the first command/bridge can run or spawn anything.
    [ConsumerJob]::Join($config.job)
    if (Test-Path -LiteralPath $config.stop) { exit 1 }
    & $config.node $config.bridge $Request
    exit $LASTEXITCODE
}

$job = [ConsumerJob]::Create($config.job)
$bootstrap = $null
try {
    $scriptPath = $PSCommandPath.Replace("'", "''")
    $requestPath = $Request.Replace("'", "''")
    $source = "& '$scriptPath' -Request '$requestPath' -JoinJob"
    $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($source))
    $start = New-Object Diagnostics.ProcessStartInfo
    $start.FileName = Join-Path $PSHOME 'powershell.exe'
    $start.Arguments = "-NoProfile -NonInteractive -EncodedCommand $encoded"
    $start.UseShellExecute = $false
    $bootstrap = [Diagnostics.Process]::Start($start)
    $bootstrapId = $bootstrap.Id
    [Console]::Error.WriteLine(('{"child_pid":' + $bootstrapId + ',"command":"windows-job-bootstrap"}'))
    $interrupted = $false
    while (!($bootstrap.WaitForExit(0))) {
        if (Test-Path -LiteralPath $config.stop) { $interrupted = $true; break }
        Start-Sleep -Milliseconds 20
    }
    $deadline = [DateTime]::UtcNow.AddMilliseconds(2000)
    $orphan = [ConsumerJob]::Shutdown($job, $deadline, $interrupted)
    $remaining = [int][Math]::Max(0, [Math]::Ceiling(($deadline - [DateTime]::UtcNow).TotalMilliseconds))
    if (!$bootstrap.WaitForExit($remaining)) { throw 'Windows Job bootstrap shutdown unconfirmed' }
    $bootstrapExitCode = $bootstrap.ExitCode
    # Failed-association accounting retains the bootstrap until its process handle closes.
    $bootstrap.Dispose()
    $bootstrap = $null
    while ([ConsumerJob]::Active($job) -gt 0) {
        if ([DateTime]::UtcNow -ge $deadline) { throw 'Windows Job shutdown unconfirmed' }
        Start-Sleep -Milliseconds 20
    }
    $result = @{
        job = $config.job; controller = $PID; active_processes = 0
        bootstrap = $bootstrapId; exit_code = $bootstrapExitCode
        interrupted = $interrupted; orphan = $orphan
    }
    [IO.File]::WriteAllText($config.result, ($result | ConvertTo-Json -Compress))
    [Console]::Error.WriteLine(('{"child_closed":' + $bootstrapId + '}'))
    if ($interrupted -or $orphan) { exit 1 }
    exit $bootstrapExitCode
} finally {
    # Missing completion receipt is never cleanup proof, even with kill-on-close.
    if (![ConsumerJob]::CloseHandle($job)) { throw 'Windows Job handle close failed' }
    if ($bootstrap) { $bootstrap.Dispose() }
}
