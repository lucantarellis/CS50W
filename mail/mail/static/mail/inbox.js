document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Send email on form submit
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-detail').style.display = 'none';
  
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // Fetch JSON data
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    emails.forEach(email => {

      const element = document.createElement('div');
      element.className = email.read ? 'email-card-read' : 'email-card';

      element.innerHTML = `<div style="display: flex;"><div style="width: 200px;"><b>${email.sender}</b></div><div style="width: auto;"><b>${email.subject}</b></div></div><div>${email.timestamp}</div>`;
      element.addEventListener('click', () => load_email(email.id));

      document.querySelector('#emails-view').append(element);

    });

    document.querySelector('#emails-view').style.display = 'block';
  })
}

function send_email(event) {
  event.preventDefault();
  
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(() => load_mailbox('inbox'));
}

function load_email(id) {

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {

    // Toggle view display
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#emails-detail').style.display = 'block';
  
    // Clean email-detail view
    document.querySelector('#emails-detail').innerHTML = '';

    // Create components needed
    const email_data = document.createElement('div');
    const email_body = document.createElement('div');
    const reply_btn = document.createElement('button');
    const back_btn = document.createElement('button');
    const archive_btn = document.createElement('button');
  
    // Reply button
    reply_btn.setAttribute('id', 'reply');
    reply_btn.className = 'btn btn-sm btn-primary';
    reply_btn.innerHTML = 'Reply';
    reply_btn.addEventListener('click', function() {
      compose_email();

      // Show compose view and hide other views
      document.querySelector('#emails-detail').style.display = 'none';
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';

      // Clear out composition fields
      document.querySelector('#compose-recipients').value = email.sender;

      subject = email.subject.startsWith('Re:') ? email.subject : `Re: ${email.subject}`;

      document.querySelector('#compose-subject').value = subject;
      document.querySelector('#compose-body').value = `--- On ${email.timestamp}, ${email.sender} wrote: ${email.body} ---`;
    })
  
    // Back button
    back_btn.setAttribute('id', 'back');
    back_btn.className = 'btn btn-sm btn-outline-primary';
    back_btn.innerHTML = 'Go back';
    back_btn.addEventListener('click', () => load_mailbox('inbox'));
  
    // Archive button
    archive_btn.setAttribute('id', 'archive');
    archive_btn.className = 'btn btn-sm btn-outline-danger';
    archive_btn.innerHTML = email.archived ? 'Unarchive' : 'Archive';
    archive_btn.addEventListener('click', () => {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !email.archived
        })
      })
      .then(() => load_mailbox('inbox'))
    })

    email_data.innerHTML = `
    <li><b>From: </b>${email.sender}</li>
    <li><b>To: </b>${email.recipients}</li>
    <li><b>Subject: </b>${email.subject}</li>
    <li><b>Date: </b>${email.timestamp}</li>
    `;

    email_body.innerHTML = `
    <hr>
    <tr>${email.body}</tr>
    `;

    // Render components
    document.querySelector('#emails-detail').append(back_btn);
    document.querySelector('#emails-detail').append(archive_btn);
    document.querySelector('#emails-detail').append(email_data);
    document.querySelector('#emails-detail').append(reply_btn);
    document.querySelector('#emails-detail').append(email_body);

    // Mark email as read
    if (email.read == false) {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
    }
  })
}
