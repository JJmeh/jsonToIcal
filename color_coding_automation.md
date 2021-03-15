function ColorEvents() {

  var today = new Date();
  var nextmonth = new Date();
  nextmonth.setDate(nextmonth.getDate() + 30);
  Logger.log(today + " " + nextmonth);

  var calendars = CalendarApp.getAllOwnedCalendars();
  Logger.log("found number of calendars: " + calendars.length);

  for (var i=0; i<calendars.length; i++) {
    var calendar = calendars[i];
    var events = calendar.getEvents(today, nextmonth);
    for (var j=0; j<events.length; j++) {
      var e = events[j];
      var title = e.getTitle();
      Logger.log(title);
      if (title[0] == "[") {
        e.setColor(CalendarApp.EventColor.GREEN);
      }
      if (title[0] == "{") {
        e.setColor(CalendarApp.EventColor.RED);
      }
      if (title[0] == "(") {
        e.setColor(CalendarApp.EventColor.ORANGE);
      }
    }
  }
}
