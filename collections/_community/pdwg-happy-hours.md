---
title: PDWG Happy Hours
description: This page lists information about upcoming and past meetings of the Paleo Data Working Group.
layout: faceted
facet_data: pdwg-happy-hours
facet_keys: [date, topics]
status: published
contributors: []
last_modified_at: 2025-09-15
---

The Paleo Data Working Group “happy hours” are informal, biweekly discussions about various different topics, including those related to data standards for paleontology collections, digitizing collections, and general collections management. Discussion topics are collaboratively developed, presented, and discussed by working group members, and supplemented with invited speakers when appropriate. No registration is required and anyone is welcome to attend. Happy hours occur every other Thursday at 12pm Eastern (UTC-5), and the Zoom link to join is distributed via our [email list](https://groups.google.com/g/paleo-data/about) and [Slack workspace](https://join.slack.com/t/paleo-data/shared_invite/zt-wtdqsnid-6Xe6cja4YuzFqmzIKfKzHw) prior to each meeting.

<h2>Upcoming Events</h2>
<table class="events faceted">
  <tr>
    <th>Date</th>
    <th>Title</th>
    <th>Notes</th>
    <th>Recording</th>
  </tr>
{% capture now %}{{ "now" | date: "%Y-%m-%d" }}{% endcapture %}
{% assign items = site.data[page.facet_data] | sort: "date" %}
{% for item in items %}
  {% capture then %}{{ item.date | date: "%Y-%m-%d" }}{% endcapture %}
  {% if then >= now %}
    <tr id="{{ item.date }}" data-tags="{{ item.date | date: '%Y'}}|{{ item.topics | join: '|'}}">
      <td>{{ item.date }}</td>
      <td>{{ item.title }}</td>
      <td>{% if item.notes %}<a href="{{ item.notes }}"><img class="icon" src="{{ '/assets/images/ri--file-text-line.png' | relative_url }}"></a>{% endif %}</td>
      <td>{% if item.recording %}<a href="{{ item.recording }}"><img class="icon" src="{{ '/assets/images/ri--video-on-line.png' | relative_url }}"></a>{% endif %}</td>
    </tr>
   {% endif %}
{% endfor %}
</table>

<h2>Past Events</h2>
<table class="events faceted">
  <tr>
    <th>Date</th>
    <th>Title</th>
    <th>Notes</th>
    <th>Recording</th>
  </tr>
{% capture now %}{{ "now" | date: "%Y-%m-%d" }}{% endcapture %}
{% assign items = site.data[page.facet_data] | sort: "date" | reverse %}
{% for item in items %}
  {% capture then %}{{ item.date | date: "%Y-%m-%d" }}{% endcapture %}
  {% if then < now %}
    <tr id="{{ item.date }}" data-tags="{{ item.date | date: '%Y'}}|{{ item.topics | join: '|'}}">
      <td>{{ item.date }}</td>
      <td>{{ item.title }}</td>
      <td>{% if item.notes %}<a href="{{ item.notes }}"><img class="icon" src="{{ '/assets/images/ri--file-text-line.png' | relative_url }}"></a>{% endif %}</td>
      <td>{% if item.recording %}<a href="{{ item.recording }}"><img class="icon" src="{{ '/assets/images/ri--video-on-line.png' | relative_url }}"></a>{% endif %}</td>
    </tr>
   {% endif %}
{% endfor %}
</table>
