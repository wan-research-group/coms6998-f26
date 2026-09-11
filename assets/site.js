/* COMS 6998 site behavior: theme toggle, current-week highlight,
   optional-readings expand/collapse, print handling. No dependencies. */
(function () {
  "use strict";

  /* ------------------------------------------------ theme toggle */
  var root = document.documentElement;
  var toggle = document.getElementById("theme-toggle");

  function systemDark() {
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  function currentTheme() {
    return root.getAttribute("data-theme") || (systemDark() ? "dark" : "light");
  }
  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("cs6998-theme", next); } catch (e) {}
    });
  }

  /* ------------------------------------------------ current-week highlight
     A week is "current" from the Saturday after the previous class through
     its own Friday. Past weeks are dimmed. The instructor can pin a week by
     setting `current_week: N` in data/schedule.yaml. */
  var container = document.querySelector(".weeks");
  if (container) {
    var rows = Array.prototype.slice.call(container.querySelectorAll(".week[data-date]"));
    var today = new Date();
    today.setHours(0, 0, 0, 0);

    var pinned = container.getAttribute("data-current-week");
    var current = null;

    rows.forEach(function (row) {
      var d = new Date(row.getAttribute("data-date") + "T23:59:59");
      if (d < today) row.classList.add("past");
    });

    if (pinned) {
      current = document.getElementById("week-" + pinned);
    } else {
      for (var i = 0; i < rows.length; i++) {
        if (rows[i].hasAttribute("data-noclass")) continue;
        var d = new Date(rows[i].getAttribute("data-date") + "T23:59:59");
        if (d >= today) { current = rows[i]; break; }
      }
      // Only highlight once the semester is near/underway (within 8 days).
      if (current) {
        var cd = new Date(current.getAttribute("data-date") + "T00:00:00");
        if ((cd - today) / 86400000 > 8) current = null;
      }
    }

    if (current) {
      current.classList.remove("past");
      current.classList.add("current");
      var chip = current.querySelector(".chip-now");
      if (chip) chip.hidden = false;
    }
  }

  /* ------------------------------------------------ homepage Now panel */
  var nowSection = document.getElementById("now");
  if (nowSection) {
    var nowMoment = new Date();
    var todayStart = new Date(nowMoment.getFullYear(), nowMoment.getMonth(), nowMoment.getDate());
    var classCards = Array.prototype.slice.call(nowSection.querySelectorAll(".now-class[data-date]"));
    var selectedClass = null;

    classCards.forEach(function (card) { card.hidden = true; });
    for (var n = 0; n < classCards.length; n++) {
      var classDate = new Date(classCards[n].getAttribute("data-date") + "T23:59:59");
      if (classDate >= nowMoment) { selectedClass = classCards[n]; break; }
    }
    if (!selectedClass && classCards.length) selectedClass = classCards[classCards.length - 1];
    if (selectedClass) {
      selectedClass.hidden = false;
      var state = selectedClass.querySelector(".now-state");
      var selectedDate = new Date(selectedClass.getAttribute("data-date") + "T00:00:00");
      var daysAway = Math.round((selectedDate - todayStart) / 86400000);
      if (state) state.textContent = daysAway < 0 ? "Course complete" : (daysAway <= 6 ? "This week" : "Next class");
    }

    var deadlineItems = Array.prototype.slice.call(nowSection.querySelectorAll(".now-deadline-item[data-due]"));
    var selectedDeadline = null;
    deadlineItems.forEach(function (item) { item.hidden = true; });
    for (var m = 0; m < deadlineItems.length; m++) {
      if (new Date(deadlineItems[m].getAttribute("data-due")) >= nowMoment) {
        selectedDeadline = deadlineItems[m];
        break;
      }
    }
    if (selectedDeadline) selectedDeadline.hidden = false;
    var noDeadline = document.getElementById("now-no-deadline");
    if (noDeadline) noDeadline.hidden = !!selectedDeadline;
  }

  /* ------------------------------------------------ optionals expand/collapse */
  function revealLinkedOptional() {
    var id = window.location.hash.slice(1);
    if (id.indexOf("optional-week-") !== 0) return;
    var detail = document.getElementById(id);
    if (detail && detail.matches("details.optional")) {
      detail.open = true;
      detail.scrollIntoView({ block: "start" });
    }
  }
  revealLinkedOptional();
  window.addEventListener("hashchange", revealLinkedOptional);

  var btn = document.getElementById("toggle-optionals");
  if (btn) {
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("data-state") !== "open";
      document.querySelectorAll("details.optional").forEach(function (d) { d.open = open; });
      btn.setAttribute("data-state", open ? "open" : "closed");
      btn.textContent = open ? "Collapse optional readings" : "Expand optional readings";
    });
  }

  /* ------------------------------------------------ print: reveal collapsed content */
  var reopened = [];
  window.addEventListener("beforeprint", function () {
    reopened = [];
    document.querySelectorAll("details.optional:not([open]), details.project-brief:not([open])").forEach(function (d) {
      d.open = true;
      reopened.push(d);
    });
  });
  window.addEventListener("afterprint", function () {
    reopened.forEach(function (d) { d.open = false; });
    reopened = [];
  });
})();
