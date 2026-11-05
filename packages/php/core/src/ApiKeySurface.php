<?php

declare(strict_types=1);

namespace Qubrics\Core;

enum ApiKeySurface: string
{
    case Root = 'root';
    case Mailbox = 'mailbox';
    case Sending = 'sending';
}
