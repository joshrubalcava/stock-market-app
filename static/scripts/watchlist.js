let $deleteWatchlistButton = $('.delete-watchlist-button');

const watchlistDeletedText = '<div class="mt-4 container d-flex justify-content-center"><div class="w-80 table-responsive"><h3>No Watchlist Created</h3><p>Start a watchlist by searching for a <a class="link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover" href="/tickers">ticker</a>!</p></div></div>';

const deleteWatchlistItem = async (evt) => {
  evt.preventDefault();

  let id = $(evt.target).data('id');
  let $closestRow = $(evt.target).closest('tr');
  let res = await axios.delete(`/watchlists/${id}/delete`);

  if (res.data.watchlist === null) {
    let $watchlistContainer = $('.watchlist-container');
    if ($deleteWatchlistButton.data('route') === 'home') {
      $watchlistContainer.remove();
    } else {
      $watchlistContainer.empty();
      $watchlistContainer.append($(watchlistDeletedText));
    }
  } else {
    $closestRow.remove();
  }
}

let $deleteWatchlistItemButton = $('.delete-watchlist-item')

$deleteWatchlistItemButton.on('click', deleteWatchlistItem)

const deleteWatchlist = async (evt) => {
  evt.preventDefault();

  await axios.delete(`/watchlists/delete`);
  
  let $watchlistContainer = $('.watchlist-container');

  if ($deleteWatchlistButton.data('route') === 'home') {
    $watchlistContainer.remove();
  } else {
    $watchlistContainer.empty();
    $watchlistContainer.append($(watchlistDeletedText));
  }
}

$deleteWatchlistButton.on('click', deleteWatchlist);