<?php

declare(strict_types=1);

// phpcs:disable PSR1.Files.SideEffects

namespace Qubrics\Management\Model;

/*
 * Deprecated name of MailboxCredential, kept as a class alias until qubrics/management 3.0.
 */
@trigger_error(
    'Qubrics\Management\Model\MailboxAppPasswordResultCredential is deprecated; use '
    . 'Qubrics\Management\Model\MailboxCredential. It will be removed in qubrics/management 3.0.',
    E_USER_DEPRECATED
);
class_alias(MailboxCredential::class, __NAMESPACE__ . '\MailboxAppPasswordResultCredential');

if (false) {
    /**
     * @deprecated use MailboxCredential
     */
    class MailboxAppPasswordResultCredential extends MailboxCredential
    {
    }
}
