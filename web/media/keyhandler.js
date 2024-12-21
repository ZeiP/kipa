function checkForEnter(event) {
  switch (event.keyCode) {
    // up arrow
    case 40:
      $(this)
        .parent()
        .parent()
        .next()
        .children("td")
        .children("input[class=" + $(this).attr("class") + "]")
        .focus()
        .select();
      break;

    // down arrow
    case 38:
      $(this)
        .parent()
        .parent()
        .prev()
        .children("td")
        .children("input[class=" + $(this).attr("class") + "]")
        .focus()
        .select();
      break;

    // Enter key
    case 13:
      $(this)
        .parent()
        .parent()
        .next()
        .children("td")
        .children("input[class=" + $(this).attr("class") + "]")
        .focus()
        .select();
      event.preventDefault();
      return false;
      break;
  }
}
