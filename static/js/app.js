function starButton(postId, userId, starId=0) {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const _postId = postId;
  const _userId = userId;
  let _starId = starId;
  const element = document.querySelector(`.star.star--post-id-${_postId}`);
  if (_starId) {
    element.addEventListener('click', removeStar)
  } else {
    element.addEventListener('click', addStar)
  }

  function addStar() {
    fetch("/api/stars/",{
      method: "POST",
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
      },
      body:JSON.stringify({
          post: _postId,
          user: _userId
      })
    })
    .then(function(response) {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      console.log("status=" + response.status);
      if (response.status !== 201) {
        throw new Error(response.status);
      }
      element.textContent = 'いいね済';
      return response.json();
    })
    .then(function(data) {
      console.log(JSON.stringify(data));
      element.addEventListener('click', removeStar)
      element.removeEventListener('click', addStar)
      _starId = data['id']
    })
    .catch(function(err) {
      console.log(err);
    });
  }

  function removeStar() {
    fetch(`/api/stars/${_starId}`, {
      method: "DELETE",
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
      }
    })
    .then(function(response) {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      console.log("status=" + response.status);
      if (response.status !== 204) {
        throw new Error(response.status);
      }
      _starId = 0;
      element.textContent = 'いいねする';
      element.addEventListener('click', addStar)
      element.removeEventListener('click', removeStar)
    })
    .catch(function(err) {
      console.log(err);
    });
  }
}