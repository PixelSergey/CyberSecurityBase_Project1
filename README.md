# Cyber Security Base 2020: Project 1

The first course project for the Cyber Security Base 2020 course at the Open University of Helsinki.

The project features a basic "vault" app, where users can log in and store their own secrets along with a colour.
Users can also delete all secrets containing a certain substring.
The app is designed to simulate a broken web application with the secrets being sensitive data.

As outlined in the [course page](https://cybersecuritybase.mooc.fi/module-3.1), this project contains
a number of cybersecurity vulnerabilities from the [OWASP Top 10 list](https://owasp.org/www-project-top-ten/).
This document contains information on the implemented vulnerabilities and how to fix them.

---

## Installation instructions

1. Install the required dependencies as outlined in the
[course installation guide](https://cybersecuritybase.mooc.fi/installation-guide)
1. Clone the repository
1. Run the `first_setup.sh` or `first_setup.bat` script on Unix and Windows, repsectively
1. The server should now be started
1. Access the website by typing `localhost:8000` in your browser
1. After you are done, close the server with CTRL+C in the terminal
1. If you need to open the server again, simply execute the `run.sh` or `run.bat` script on
Unix and Windows, repsectively.

---

## Flaws

### Flaw 1: Injection

Injection vulnerabilities are the most common vulnerability on the OWASP Top 10 list.
Injection can happen when untrusted (attacker-controlled) data is sent to an interpreter.
While this can happen in many languages, it is most often found in database query languages
such as SQL.

In this project, I have implemented an SQL injection vulnerability into the vault application.
While there is no issue with adding secrets, as it uses Django's own model system, deleting a note
opens up an SQL injection attack. This is because the deletion uses the custom SQL request
`"SELECT * FROM vulns_note WHERE owner_id = {} AND text LIKE '%{}%'".format(request.user.id, text)`.
Since the raw text is subsituted into this query, an attacker can terminate it using a `'` and write
their own query afterwards. For example, submitting `' OR '%'='` into the `Remove a secret` box
will remove _all_ secrets from _all_ users, which is a huge security oversight.

Fixing this is easy: Django provides the model system which includes protections against injection
attacks. It does so by escaping "dangerous" character sequences and including other checks on untrusted
data. An example of how the system is used can be seen in the `addnote()` function of `views.py`.

### Flaw 2: Broken Authentication

TBC

### Flaw 3: Sensitive Data Exposure

TBC

### Flaw 4: Broken Access Control

TBC

### Flaw 5: Cross-Site Scripting (XSS)

XSS happens when unfiltered data is used to generate an HTML webpage which can contain JavaScript.
An XSS attack can be used to execute arbitrary code in a victim's browser.

In this project, XSS can be used when adding a secret. Adding secrets is fine in and of itself; however,
the secrets are displayed in an insecure way. To get colours to work, the function that generates `index.html`
uses the line `'<span><li style="background-color: {}">{}</li></span>'.format(note.colour, note.text)`.
Normally, this generates a tag with a colour and text. However, if the colour or text is controlled by an
attacker, arbitrary HTML can be generated. For example, adding the secret `<script>alert("hacked")</script>`
using the `Add a secret` box will run the JavaScript code when the secret is displayed. In conjunction with
Broken Access Control, XSS can be used to steal cookies and sensitive data from a user.

This can be fixed by properly escaping both the colour and text provided. Django's utilities provide a helper
function `django.utils.html.escape(text)`, which will prevent the XSS attack when rendering secrets.

---

## Credits

This project was developed by myself, with thanks to:

- Nikolaj Tatti, instructor, for clarification and help
- [@tamithia](https://github.com/tamithia) for adding CSS and graphics to the app
(authorised by Nikolaj Tatti)
