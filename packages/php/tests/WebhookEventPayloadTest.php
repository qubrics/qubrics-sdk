<?php

declare(strict_types=1);

namespace Qubrics\Tests;

use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;
use Qubrics\Management\Model\MailWebhookEventPayload;
use Qubrics\Management\Model\WebhookCreateBody;
use Qubrics\Management\Model\WebhookDeliveryAttempt;
use Qubrics\Management\Model\WebhookDeliveryPayload;
use Qubrics\Management\Model\WebhookEventData;
use Qubrics\Management\Model\WebhookEventPayload;
use Qubrics\Management\Model\WebhookSubscription;
use Qubrics\Management\Model\WebhookSubscriptionWithSecret;
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

    public function testHistoricalMailMetadataPreservesOpenLabels(): void
    {
        self::assertSame('message.received', WebhookSubscription::EVENT_TYPES_MESSAGE_RECEIVED);
        self::assertSame('message.received', WebhookSubscriptionWithSecret::EVENT_TYPES_MESSAGE_RECEIVED);
        self::assertSame('message.received', WebhookDeliveryAttempt::EVENT_TYPE_MESSAGE_RECEIVED);
        self::assertSame('message.received', WebhookDeliveryPayload::EVENT_TYPE_MESSAGE_RECEIVED);
        $knownLabels = [
            'message.delivered', 'message.bounced', 'message.complained', 'message.rejected',
            'message.delivery_delayed', 'message.received', 'message.received.spam', 'sendmux.test',
            'unknown_default_open_api',
        ];

        foreach ([new WebhookSubscription(), new WebhookSubscriptionWithSecret()] as $subscription) {
            self::assertSame($knownLabels, $subscription::getEventTypesAllowableValues());
            self::assertFalse(defined($subscription::class . '::EVENT_TYPES_CALENDAR_CHANGED'));
            $labels = ['message.received', 'calendar.changed', 'future.event'];
            self::assertSame($labels, $subscription->setEventTypes($labels)->getEventTypes());
            self::assertStringNotContainsString(
                "for 'event_types'",
                implode('; ', $subscription->listInvalidProperties())
            );
        }
        foreach ([new WebhookDeliveryAttempt(), new WebhookDeliveryPayload()] as $delivery) {
            self::assertSame($knownLabels, $delivery::getEventTypeAllowableValues());
            self::assertFalse(defined($delivery::class . '::EVENT_TYPE_CALENDAR_CHANGED'));
            foreach (['message.received', 'calendar.changed', 'future.event'] as $label) {
                self::assertSame($label, $delivery->setEventType($label)->getEventType());
                self::assertStringNotContainsString(
                    "for 'event_type'",
                    implode('; ', $delivery->listInvalidProperties())
                );
            }
        }
    }

    public function testNewSubscriptionRejectsCalendarLabel(): void
    {
        self::assertNotContains('calendar.changed', WebhookCreateBody::getEventTypesAllowableValues());
        $this->expectException(\InvalidArgumentException::class);
        (new WebhookCreateBody())->setEventTypes(['calendar.changed']);
    }

    public function testUnknownDiscriminatorKeepsBaseModelFallback(): void
    {
        $event = ObjectSerializer::deserialize((object) ['type' => 'future.event'], WebhookEventPayload::class);

        self::assertInstanceOf(WebhookEventPayload::class, $event);
        self::assertSame('unknown_default_open_api', $event->getType());
        self::assertFalse($event->valid());
    }
}
