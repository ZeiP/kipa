function checkForEnter(event) {
  switch (event.originalEvent.key) {
    case "ArrowUp":
      $(this)
        .parent()
        .parent()
        .prev()
        .children("td")
        .children("input[class=" + $(this).attr("class") + "]")
        .focus()
        .select();
      break;

    case "ArrowDown":
      $(this)
        .parent()
        .parent()
        .next()
        .children("td")
        .children("input[class=" + $(this).attr("class") + "]")
        .focus()
        .select();
      break;

    case "Enter":
      $(this)
        .parent()
        .parent()
        .next()
        .children("td")
        .children("input[class=" + $(this).attr("class") + "]")
        .focus()
        .select();
      event.preventDefault();
  }
}
