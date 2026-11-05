<?php

declare(strict_types=1);

namespace Qubrics\Tests;

use Qubrics\Management\Model\ManagementCreateMailboxRequest;
use Qubrics\Management\Model\WebhookEventPayload;
use PHPUnit\Framework\TestCase;

final class ManagementValidationTest extends TestCase
{
    public function testWebhookDiscriminatorPreservesEveryWireValue(): void
    {
        $payload = new WebhookEventPayload();
        foreach (
            [
                'calendar.changed',
                'message.bounced',
                'message.complained',
                'message.delivered',
                'message.delivery_delayed',
                'message.received',
                'message.received.spam',
                'message.rejected',
                'sendmux.test',
            ] as $type
        ) {
            self::assertContains($type, WebhookEventPayload::getTypeAllowableValues());
            self::assertSame($type, $payload->setType($type)->getType());
        }
        self::assertSame('unknown_default_open_api', $payload->setType('future.event')->getType());
    }

    public function testMailboxEmailValidationRejectsLineBreaks(): void
    {
        foreach (["agent@example.com\n", "agent@example.com\r", "agent@example.com\r\n"] as $email) {
            $request = new ManagementCreateMailboxRequest(['email' => $email]);

            self::assertFalse($request->valid(), sprintf('Expected %s to be rejected', json_encode($email)));
        }
    }

    public function testMailboxEmailValidationAcceptsAValidFullValue(): void
    {
        $request = new ManagementCreateMailboxRequest(['email' => 'agent@example.com']);

        self::assertTrue($request->valid());
        self::assertSame('agent@example.com', $request->getEmail());
    }
}
