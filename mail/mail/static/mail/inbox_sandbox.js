document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);
  
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
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#emails-detail').style.display = 'none';
  
    // Fetch JSON data
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      emails.forEach(email => {
        const element = document.createElement('div');
        element.classList.add('email-card');
        element.innerHTML = `<div style="display: flex;"><div style="width: 200px;"><b>${email.sender}</b></div><div style="width: auto;"><b>${email.subject}</b></div></div><div>${email.timestamp}</div>`;
        element.addEventListener('click', (email_detail) => {
          fetch(`/emails/${email_detail.id}`, {
            method: 'PUT',
            body: JSON.stringify({
              read: true
            })
          })
          load_email(email_detail);
        });
        document.querySelector('#emails-view').append(element);
      })
    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
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
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result);
    })
    load_mailbox('sent');
  }
  
  function load_email(email) {
    // Toggle view display
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#emails-detail').style.display = 'block';
  
    // Fetch email
    fetch(`/emails/${email.id}`)
    .then(response => response.json())
    .then(email => {
      const email_body = document.createElement('div');
      email_body.innerHTML = `<div>${email.sender}</div><div>${email.subject}</div><div>${email.timestamp}</div><div>${email.body}`
    })
  }



    // Flag email as read
    fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })


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
        document.querySelector('#emails-view').style.display = 'block';
        document.querySelector('#compose-view').style.display = 'none';
        document.querySelector('#emails-detail').style.display = 'none';
      
        // Fetch JSON data
        fetch(`/emails/${mailbox}`)
        .then(response => response.json())
        .then(emails => {
          emails.forEach(email => {
            const element = document.createElement('div');
            if (email.read == true) {
              element.classList.add('email-card-read');
            } else {
              element.classList.add('email-card');
            }
            if (email.archived != true) {
              element.innerHTML = `<div style="display: flex;"><div style="width: 200px;"><b>${email.sender}</b></div><div style="width: auto;"><b>${email.subject}</b></div></div><div>${email.timestamp}</div>`;
              element.addEventListener('click', () => load_email(email.id));
            }
            document.querySelector('#emails-view').append(element);
          });
        })
      
        // Show the mailbox name
        document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
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
        .then(response => response.json())
        .then(result => {
          // Print result
          console.log(result);
        })
      }
      
      function load_email(id) {
      
      // Mark email as read
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        })
      
        // Toggle view display
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'none';
        document.querySelector('#emails-detail').style.display = 'block';
      
        // Clean email-detail view
        document.querySelector('#emails-detail').innerHTML = '';
      
        // Create components needed
        const email_body = document.createElement('div');
        const reply_btn = document.createElement('button');
        const back_btn = document.createElement('button');
        const archive_btn = document.createElement('button');
      
        // Reply button
        reply_btn.setAttribute('id', 'reply');
        reply_btn.classList.add = 'btn btn-sm btn-outline-primary';
        reply_btn.innerHTML = 'Reply';
      
        // Back button
        back_btn.setAttribute('id', 'back');
        back_btn.classList.add = 'btn btn-sm btn-outline-primary';
        back_btn.innerHTML = 'Go back';
        back_btn.addEventListener('click', () => load_mailbox('inbox'));
      
        // Archive button
        archive_btn.setAttribute('id', 'archive');
        archive_btn.classList.add = 'btn btn-sm btn-outline-primary';
        archive_btn.innerHTML = 'Archive';
        archive_btn.addEventListener('click', () => {
          fetch(`/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: true
            })
          })
          load_mailbox('archive');
        })
        
        // Fetch email
        fetch(`/emails/${id}`)
        .then(response => response.json())
        .then(email => {
          email_body.innerHTML = `
          <div>${email.sender}</div>
          <div>${email.subject}</div>
          <div>${email.timestamp}</div>
          <div>${email.body}</div>
          `;
        })
      
        document.querySelector('#emails-detail').append(back_btn);
        document.querySelector('#emails-detail').append(archive_btn);
        document.querySelector('#emails-detail').append(email_body);
        document.querySelector('#emails-detail').append(reply_btn);
      }





      function reply(replyto) {
        // Show compose view and hide other views
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'block';
      
        // Clear out composition fields
        document.querySelector('#compose-recipients').value = `${replyto}`;
        document.querySelector('#compose-subject').value = '';
        document.querySelector('#compose-body').value = '';
      }