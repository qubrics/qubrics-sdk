<?php

declare(strict_types=1);

namespace Qubrics\Tests;

use Composer\InstalledVersions;
use PHPUnit\Framework\TestCase;
use Qubrics\Core\ApiKeySurface;
use Qubrics\Core\Auth;
use Qubrics\Core\QubricsApiError;
use Qubrics\Mailbox\ClientFactory as MailboxFactory;
use Qubrics\Management\ClientFactory as ManagementFactory;
use Qubrics\Management\Model\WebhookEventData;
use Qubrics\Sending\ClientFactory as SendingFactory;
use Qubrics\Sdk\Sdk;

final class QubricsPackagesTest extends TestCase
{
    public function testComposerLoadsRenamedPackagesAndDefaults(): void
    {
        foreach (['core', 'sending', 'mailbox', 'management', 'sdk'] as $package) {
            self::assertTrue(InstalledVersions::isInstalled('qubrics/' . $package));
        }

        self::assertSame('3.0.0', Sdk::VERSION);
        self::assertTrue(class_exists(QubricsApiError::class));
        Auth::assertApiKeySurface('smx_root_test', ApiKeySurface::Root);
        self::assertSame('https://smtp.qubrics.com/api/v1', SendingFactory::configuration('smx_mbx_test')->getHost());
        self::assertSame('https://app.qubrics.com/api/v1', MailboxFactory::configuration('smx_mbx_test')->getHost());
        self::assertSame(
            'https://app.qubrics.com/api/v1',
            ManagementFactory::configuration('smx_root_test')->getHost()
        );
    }

    public function testBothMessageIdContractsSurviveNamespaceRename(): void
    {
        $data = new WebhookEventData(['sendmux_message_id' => 'legacy', 'qubrics_message_id' => 'current']);

        self::assertSame('legacy', $data->getSendmuxMessageId());
        self::assertSame('current', $data->getQubricsMessageId());
        self::assertSame('sendmux_message_id', WebhookEventData::attributeMap()['sendmux_message_id']);
        self::assertSame('qubrics_message_id', WebhookEventData::attributeMap()['qubrics_message_id']);
    }
}
