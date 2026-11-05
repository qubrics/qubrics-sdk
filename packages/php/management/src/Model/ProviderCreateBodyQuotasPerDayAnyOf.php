<?php

declare(strict_types=1);

// phpcs:disable PSR1.Files.SideEffects

namespace Qubrics\Management\Model;

/*
 * Deprecated name of ProviderQuotaRange, kept as a class alias until qubrics/management 3.0.
 */
@trigger_error(
    'Qubrics\Management\Model\ProviderCreateBodyQuotasPerDayAnyOf is deprecated; use '
    . 'Qubrics\Management\Model\ProviderQuotaRange. It will be removed in qubrics/management 3.0.',
    E_USER_DEPRECATED
);
class_alias(ProviderQuotaRange::class, __NAMESPACE__ . '\ProviderCreateBodyQuotasPerDayAnyOf');

if (false) {
    /**
     * @deprecated use ProviderQuotaRange
     */
    class ProviderCreateBodyQuotasPerDayAnyOf extends ProviderQuotaRange
    {
    }
}
