let show = false;

// show/hide dropdown menu
$('.profile').on('click', () => {
  if(show === false) {
    $('.drop-container').show()
    show = true;
  } else {
      $('.drop-container').hide()
      show = false;
  }
});
