$deleteWatchlistItem = $('.delete-watchlist-item');

const handleWatchlistItemDelete = (evt) => {
  evt.preventDefault();

  id = $itemId = $(this).data('id');
  console.log(id);

  $('.id').remove()
};

$deleteWatchlistItem.submit(handleWatchlistItemDelete);