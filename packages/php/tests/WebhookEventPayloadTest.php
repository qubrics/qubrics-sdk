<?php

declare(strict_types=1);

namespace Qubrics\Tests;

use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;
use Qubrics\Management\Model\MailWebhookEventPayload;
use Qubrics\Management\Model\WebhookDeliveryPayload;
use Qubrics\Management\Model\WebhookEventData;
use Qubrics\Management\Model\WebhookEventPayload;
use Qubrics\Management\ObjectSerializer;

final class WebhookEventPayloadTest extends TestCase
{
    /** @return iterable<string, array{string}> */
    public static function mailEventTypes(): iterable
    {
        $types = [
            'message.bounced',
            'message.complained',
            'message.delivered',
            'message.delivery_delayed',
            'message.received',
            'message.received.spam',
            'message.rejected',
            'sendmux.test',
        ];
        foreach ($types as $type) {
            yield $type => [$type];
        }
    }

    #[DataProvider('mailEventTypes')]
    public function testMailDiscriminatorPreservesMailData(string $type): void
    {
        $event = ObjectSerializer::deserialize((object) [
            'id' => 'evt_fixture',
            'type' => $type,
            'team_public_id' => 'team_fixture',
            'occurred_at' => '2026-05-21T09:12:00Z',
            'data' => (object) [
                'message_id' => 'message@example.com',
                'message_id_kind' => 'rfc5322',
                'sender' => 'sender@example.com',
                'recipients' => ['inbox@example.com'],
            ],
        ], WebhookEventPayload::class);

        self::assertInstanceOf(MailWebhookEventPayload::class, $event);
        self::assertSame($type, $event->getType());
        $data = $event->getData();
        self::assertInstanceOf(WebhookEventData::class, $data);
        self::assertSame('message@example.com', $data->getMessageId());
        self::assertSame('sender@example.com', $data->getSender());
        self::assertSame(['inbox@example.com'], $data->getRecipients());
    }

    public function testRetainedDeliveryPreservesOpaquePayloadAndLabel(): void
    {
        $payload = (object) [
            'type' => 'calendar.changed',
            'data' => (object) ['opaque' => ['retained', (object) ['unknown' => true]]],
        ];
        $delivery = ObjectSerializer::deserialize((object) [
            'created_at' => '2026-11-20T00:00:00Z',
            'delivery_attempt' => 1,
            'event_id' => 'evt_retained',
            'event_type' => 'calendar.changed',
            'expires_at' => '2026-11-21T00:00:00Z',
            'id' => 'delivery_retained',
            'payload' => $payload,
        ], WebhookDeliveryPayload::class);

        self::assertInstanceOf(WebhookDeliveryPayload::class, $delivery);
        self::assertSame('calendar.changed', $delivery->getEventType());
        self::assertSame(
            json_decode(json_encode($payload, JSON_THROW_ON_ERROR), true),
            json_decode(json_encode($delivery->getPayload(), JSON_THROW_ON_ERROR), true)
        );
        $encoded = ObjectSerializer::sanitizeForSerialization($delivery);
        self::assertInstanceOf(\stdClass::class, $encoded);
        self::assertSame(
            json_decode(json_encode($payload, JSON_THROW_ON_ERROR), true),
            json_decode(json_encode($encoded->payload, JSON_THROW_ON_ERROR), true)
        );
    }

    public function testUnknownDiscriminatorKeepsBaseModelFallback(): void
    {
        $event = ObjectSerializer::deserialize((object) ['type' => 'future.event'], WebhookEventPayload::class);

        self::assertInstanceOf(WebhookEventPayload::class, $event);
        self::assertSame('unknown_default_open_api', $event->getType());
        self::assertFalse($event->valid());
    }
}
