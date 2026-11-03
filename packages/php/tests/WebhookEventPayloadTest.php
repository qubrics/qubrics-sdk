<?php

declare(strict_types=1);

namespace Sendmux\Tests;

use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;
use Sendmux\Management\Model\CalendarWebhookEventData;
use Sendmux\Management\Model\CalendarWebhookEventPayload;
use Sendmux\Management\Model\MailWebhookEventPayload;
use Sendmux\Management\Model\WebhookDeliveryPayload;
use Sendmux\Management\Model\WebhookEventData;
use Sendmux\Management\Model\WebhookEventPayload;
use Sendmux\Management\ObjectSerializer;

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
        $delivery = ObjectSerializer::deserialize((object) ['payload' => (object) [
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
        ]], WebhookDeliveryPayload::class);

        self::assertInstanceOf(WebhookDeliveryPayload::class, $delivery);
        $event = $delivery->getPayload();
        self::assertInstanceOf(MailWebhookEventPayload::class, $event);
        self::assertSame($type, $event->getType());
        $data = $event->getData();
        self::assertInstanceOf(WebhookEventData::class, $data);
        self::assertSame('message@example.com', $data->getMessageId());
        self::assertSame('sender@example.com', $data->getSender());
        self::assertSame(['inbox@example.com'], $data->getRecipients());
    }

    public function testCalendarDiscriminatorPreservesCalendarData(): void
    {
        $delivery = ObjectSerializer::deserialize((object) ['payload' => (object) [
            'type' => 'calendar.changed',
            'data' => (object) [
                'mailbox_id' => 'mbx_fixture',
                'resource' => 'event',
                'created' => ['event_created'],
                'updated' => [],
                'destroyed' => ['event_destroyed'],
                'old_state' => 'before',
                'new_state' => 'after',
                'has_more' => false,
                'sync_required' => true,
            ],
        ]], WebhookDeliveryPayload::class);

        self::assertInstanceOf(WebhookDeliveryPayload::class, $delivery);
        $event = $delivery->getPayload();
        self::assertInstanceOf(CalendarWebhookEventPayload::class, $event);
        self::assertSame('calendar.changed', $event->getType());
        $data = $event->getData();
        self::assertInstanceOf(CalendarWebhookEventData::class, $data);
        self::assertSame(['event_created'], $data->getCreated());
        self::assertSame(['event_destroyed'], $data->getDestroyed());
        self::assertSame('after', $data->getNewState());
        self::assertFalse($data->getHasMore());
        self::assertTrue($data->getSyncRequired());
    }

    public function testUnknownDiscriminatorKeepsBaseModelFallback(): void
    {
        $event = ObjectSerializer::deserialize((object) ['type' => 'future.event'], WebhookEventPayload::class);

        self::assertInstanceOf(WebhookEventPayload::class, $event);
        self::assertSame('unknown_default_open_api', $event->getType());
        self::assertFalse($event->valid());
    }
}
