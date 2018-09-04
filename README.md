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
