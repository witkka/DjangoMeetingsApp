=========================================================================
meetings_app api, version '1.0.0', March, 2022.
This is README.txt,  user guide.
Author: Katarzyna Witkowska, https://github.com/witkka
=========================================================================

Simple django app for creating, editing, deleting and viewing meetings.
This project contains following components:
- 'meetings_app' responsible for basic configuration and urls
- 'meetings' responsible for creating entries in database: table 'meeting'
containing the following columns: title, date, start_time, end_time, room,
author, participants; table 'room' containing the following columns: name,
number, floor

-------------------------------------------------------------------------
User guide:
./
Home page, for logged-in users displays all future meetings and main menu.
All future meetings are displayed as links to ./meetings/{id}
For not logged users, displays main menu and message.

./meetings/{id}
Shows data of a meeting with chosen id number.
All user can view existing meetings.
Only author of a given meeting can change or delete this meeting

./meetings/new
Logged-in user can create new meeting by entering data into a form.
title: what this meeting is about;
date: chosen from the datetime widget;
start time: entered manually;
room: chosen from the dropdown menu;
participants: chosen from the dropdown menu
Meetings cannot be booked for past dates or if chosen rooms are booked in
chosen time slots.

./meetings/edit
Available only to the author of a particular meeting. Author can change all parameters,
except for meeting id. Meeting cannot be chosen for past dates.

./meetings/delete
Available only to the author of a particular meeting. Author can delete chosen meeting.

./meetings/confirmation
Page with information, that chosen meeting has been deleted.

./meetings/search
All users can search for meetings existing in database. Query results are
displayed as a clickable list. To perform a query, necessary is only one field
filled in.

Search form contains:
title: app searches for all meetings containing given keywords;
author: author's name;
room: chosen from a dropdown menu;
time ranged: day from, to; time from, to - chosen from widgets
search button






