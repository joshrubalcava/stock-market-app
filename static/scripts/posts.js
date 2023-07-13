const deletePost = async (evt) => {
  evt.preventDefault();

  let $postId = $(evt.target).data('id');
  let $ticker = $(evt.target).data('ticker');
  let res = await axios.delete(`/tickers/${$ticker}/post/${$postId}/delete`);

  let $postsContainer = $('.posts-container');

  if (res.data.posts === null) {
    if ($deletePostButton.data('route') === 'ticker-details') {
      $postsContainer.empty();
      $postsContainer.append(`<div class="posts-container"><h3 class="mb-3">No Posts Yet.</h3><a href="/tickers/${$ticker}/post/add" class="btn btn-info">Add Post</a></div>`);
    } else {
      $postsContainer.empty();
      $postsContainer.append('<div class="posts-container"><h3>No Posts Yet!</h3></div>');
    }
  } else {
    $postsContainer = $(`.${$postId}`);
    $postsContainer.remove();
  }
}
let $deletePostButton = $('.delete-post-button');
$deletePostButton.on('click', deletePost);