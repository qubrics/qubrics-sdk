<?php

declare(strict_types=1);

namespace Qubrics\Tests;

use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;
use ReflectionClass;
use Qubrics\Mailbox\Model\MailboxMessageContentResponse;
use Qubrics\Mailbox\Model\MailboxRawBodyResponse;
use Qubrics\Mailbox\Model\MailboxSubmissionEnvelope;
use Qubrics\Mailbox\Model\MailboxThreadContentResponse;
use Qubrics\Management\Model\MailboxAppPasswordResult;

final class DeprecatedModelAliasesTest extends TestCase
{
    /**
     * Names the nullable-reference schema shape drops from the generated packages. Each is a real
     * generated class until that regeneration lands and a deprecated class alias of the class that
     * types the same property afterwards; either way the name keeps loading.
     *
     * The declared type is null when no generated property is typed by the name (the per-day quota
     * union is flattened, so its former member class is not referenced by any property).
     *
     * @return iterable<string, array{string, string, string, mixed}>
     */
    public static function compatModelNames(): iterable
    {
        yield 'mailbox message content response data' => [
            'Qubrics\Mailbox\Model\MailboxMessageContentResponseAllOfData',
            'Qubrics\Mailbox\Model\MailboxMessageContent',
            'qubrics/mailbox 4.0',
            MailboxMessageContentResponse::openAPITypes()['data'] ?? null,
        ];
        yield 'mailbox raw body response data' => [
            'Qubrics\Mailbox\Model\MailboxRawBodyResponseAllOfData',
            'Qubrics\Mailbox\Model\MailboxRawBody',
            'qubrics/mailbox 4.0',
            MailboxRawBodyResponse::openAPITypes()['data'] ?? null,
        ];
        yield 'mailbox submission envelope recipient' => [
            'Qubrics\Mailbox\Model\MailboxSubmissionEnvelopeRcptToInner',
            'Qubrics\Mailbox\Model\MailboxSubmissionEnvelopeAddress',
            'qubrics/mailbox 4.0',
            MailboxSubmissionEnvelope::openAPITypes()['rcpt_to'] ?? null,
        ];
        yield 'mailbox thread content response data' => [
            'Qubrics\Mailbox\Model\MailboxThreadContentResponseAllOfData',
            'Qubrics\Mailbox\Model\MailboxMessageContent',
            'qubrics/mailbox 4.0',
            MailboxThreadContentResponse::openAPITypes()['data'] ?? null,
        ];
        yield 'management app password credential' => [
            'Qubrics\Management\Model\MailboxAppPasswordResultCredential',
            'Qubrics\Management\Model\MailboxCredential',
            'qubrics/management 3.0',
            MailboxAppPasswordResult::openAPITypes()['credential'] ?? null,
        ];
        yield 'management per-day quota range' => [
            'Qubrics\Management\Model\ProviderCreateBodyQuotasPerDayAnyOf',
            'Qubrics\Management\Model\ProviderQuotaRange',
            'qubrics/management 3.0',
            null,
        ];
    }

    #[DataProvider('compatModelNames')]
    public function testCompatModelNameKeepsLoadingAsTheClassTypingItsProperty(
        string $deprecated,
        string $replacement,
        string $removedIn,
        mixed $declaredType
    ): void {
        $deprecations = [];
        set_error_handler(static function (int $severity, string $message) use (&$deprecations): bool {
            if ($severity !== E_USER_DEPRECATED) {
                return false;
            }
            $deprecations[] = $message;
            return true;
        });
        try {
            $loaded = class_exists($deprecated);
        } finally {
            restore_error_handler();
        }
        self::assertTrue($loaded, "$deprecated must keep loading");
        self::assertTrue(class_exists($deprecated)); // already loaded: narrows the name without a second autoload
        $resolved = (new ReflectionClass($deprecated))->getName();

        if ($resolved === $deprecated) {
            self::assertSame([], $deprecations);
        } else {
            self::assertSame($replacement, $resolved);
            self::assertSame(
                ["$deprecated is deprecated; use $replacement. It will be removed in $removedIn."],
                $deprecations
            );
        }

        if ($declaredType === null) {
            return;
        }
        self::assertIsString($declaredType);
        $declaredClass = ltrim(rtrim($declaredType, '[]'), '\\');
        self::assertTrue(class_exists($declaredClass));
        self::assertSame($resolved, (new ReflectionClass($declaredClass))->getName());
    }
}
