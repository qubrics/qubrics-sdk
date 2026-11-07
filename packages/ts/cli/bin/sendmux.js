#!/usr/bin/env node

import { writeSync } from "node:fs";

writeSync(2, "sendmux is deprecated. Use qubrics instead.\n");
await import("./run.js");
