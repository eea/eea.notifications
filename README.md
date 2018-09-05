# eea.notifications
Let your users to be notified about the content they are interested in.

<kbd>
  <img src="https://github.com/eea/eea.notifications/blob/master/docs/mockup.png" title="Mockup" alt="Mockup" />
</kbd>


## :book: Usage

### :baby: Simple user

#### An user creates a subscription and manages his/hers subscriptions (in /@@manage_subscriptions form).

<kbd>
  <img src="https://github.com/eea/eea.notifications/blob/master/docs/manage-subscriptions-form.png" title="Manage subscriptions form" alt="Manage subscriptions form" />
</kbd>


An example subscription is "notify me on new content created that is tagged ..." (which includes both new content with interest tag, or old content that gets the interest tag), "notify me on any changes that affect content with interest tag".

### :man: Admin user

#### Administator sets content rules to ping RabbitMQ on content changes.

#### :mailbox_with_mail: Content rules for RabbitMQ pings

This means in /@@rules-controlpanel you will add a rule for each case. Examples: when an object is added, or modified, or removed...

<kbd>
  <img src="https://github.com/eea/eea.notifications/blob/master/docs/manage-content-rules-1.png" title="Manage content rules 1" alt="Manage content rules 1" />
</kbd>

the performed action is Ping RMQ.
<kbd>
  <img src="https://github.com/eea/eea.notifications/blob/master/docs/manage-content-rules-2.png" title="Manage content rules 2" alt="Manage content rules 2" />
</kbd>

Defined something like:
<kbd>
  <img src="https://github.com/eea/eea.notifications/blob/master/docs/manage-content-rules-3.png" title="Manage content rules 3" alt="Manage content rules 3" />
</kbd>

Why a ping based on a content rule? The site administrator can decide for which content types this notification mechanism applies, thus applying a “sane default” for the users.

#### :mailbox_with_no_mail: Content rules for sending notifications

You can choose to send email notifications. In this case you will set a content rule with Event trigger: EEA Notifications: send notification event and this details:

<kbd>
  <img src="https://github.com/eea/eea.notifications/blob/master/docs/manage-content-rules-b-1.png" title="Manage content rules b 1" alt="Manage content rules b 1" />
</kbd>

Action: send email.
<kbd>
  <img src="https://github.com/eea/eea.notifications/blob/master/docs/manage-content-rules-b-2.png" title="Manage content rules b 2" alt="Manage content rules b 2" />
</kbd>

In email notification you can use the substitution variables:
<kbd>
  <img src="https://github.com/eea/eea.notifications/blob/master/docs/manage-content-rules-b-3.png" title="Manage content rules b 3" alt="Manage content rules b 3" />
</kbd>

as listed in this table.
<kbd>
  <img src="https://github.com/eea/eea.notifications/blob/master/docs/manage-content-rules-b-4.png" title="Manage content rules b 4" alt="Manage content rules b 4" />
</kbd>

#### Administator sets the RabbitMQ client settings (in /@@rabbitmq-client-controlpanel).

<kbd>
  <img src="https://github.com/eea/eea.notifications/blob/master/docs/rabbitmq-client-settings.png" title="RabbitMQ client settings" alt="RabbitMQ client settings" />
</kbd>

Get IP:
```console
    $ docker inspect 8b51d27e0306 | grep "IPAddress"                                                                                    4016ms  Mon 27 Aug 2018 12:08:18 PM EEST
            "SecondaryIPAddresses": null,
            "IPAddress": "",
                    "IPAddress": "172.26.0.2"

```

Instead of 8b51d27e0306 you will use the ID of rabbitmq docker container.

#### Notifications center

An asynchronous script will process the pings (retrieve them from RabbitMQ) in order to send notification for all subscribed users in that case (tag + action). 

```console
$ bin/zeo_client run bin/notifications_center
```
#### Testing

Add in buildout.cfg:
```console
parts +=
    test

[test]
recipe = zc.recipe.testrunner
defaults = ['--auto-color', '--auto-progress']
eggs =
    eea.notifications [test]
    plone.testing [test]
    plone.app.testing [test]
```

Run the tests using:
```console
./bin/test -s eea.notifications
```

Learn more: https://docs.plone.org/4/en/manage/deploying/testing_tuning/testing_and_debugging/unit_testing.html

#### Development: Testing emails (docker)

Add in your docker-compose:
```console
  postfix:
    image: eaudeweb/mailtrap
    ports:
      - "8081:80"
````

In mail settings (@@mail-controlpanel):
  SMTP server: postfix
  SMTP port: 25

then http://localhost:8081 u: mailtrap p: mailtrap

## :book: Demonstration
When we edit a folder with title "Nice folder title here" tagged with "Austria" tag, the RabbitMQ receives pings for each user that has a subscription for this tag and "edited" action.

<kbd>
  <img src="https://github.com/eea/eea.notifications/blob/master/docs/rabbitmq.png" title="RabbitMQ" alt="RabbitMQ" />
</kbd>

Then the notification center will send the notifications to users.

<kbd>
  <img src="https://github.com/eea/eea.notifications/blob/master/docs/mailtrap.png" title="Mailtrap" alt="Mailtrap" />
</kbd>

## :star: Source code

Latest source code (Plone 4 compatible): https://github.com/eea/eea.notifications/

## :copyright: Copyright and license
The Initial Owner of the Original Code is [European Environment Agency (EEA)](https://www.eea.europa.eu/). All Rights Reserved.

More details: [LICENSE file](https://github.com/eea/eea.notifications/blob/master/LICENSE).

## :moneybag: Funding

EEA - European Environment Agency (EU)
