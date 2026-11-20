use sendmux::sending::{Address, Attachment, EmailSendRequest};
use sendmux::{MailboxClient, ManagementClient, SendingClient};

#[test]
fn public_types_and_constructors_are_identical() {
    let sending: qubrics::SendingClient = SendingClient::new("smx_mbx_fixture").unwrap();
    let _: SendingClient = sending;
    let mailbox: qubrics::MailboxClient = MailboxClient::new("smx_mbx_fixture").unwrap();
    let _: MailboxClient = mailbox;
    let management: qubrics::ManagementClient = ManagementClient::new("smx_root_fixture").unwrap();
    let _: ManagementClient = management;

    let mut request = EmailSendRequest::new(
        Address::new("sender@example.test"),
        Address::new("recipient@example.test"),
        "Fixture",
        "<p>Fixture</p>",
    );
    let address: qubrics::sending::Address = Address::new("recipient@example.test");
    let _: Address = address;
    let attachment: qubrics::sending::Attachment = Attachment::base64("note.txt", "SGk=");
    request.attachments.push(attachment);
    request
        .attachments
        .push(Attachment::uploaded("att_abcdefghijklmnopqrstuvwx"));
    let canonical: qubrics::sending::EmailSendRequest = request;
    let request: EmailSendRequest = canonical;
    assert_eq!(request.attachments.len(), 2);
    let _: qubrics::SendingClient = sendmux::sending("smx_mbx_fixture").unwrap();
    let _: qubrics::MailboxClient = sendmux::mailbox("smx_mbx_fixture").unwrap();
    let _: qubrics::ManagementClient = sendmux::management("smx_root_fixture").unwrap();
}
