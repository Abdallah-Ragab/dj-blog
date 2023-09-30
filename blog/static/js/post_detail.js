function isLikedPost() {
    const postSlug = '{{ post.slug }}'
    likedPosts = JSON.parse(localStorage.getItem('likedPosts')) || []
    postIndex = likedPosts.indexOf(postSlug)
    if (postIndex === -1) {
      return false
    } else {
      return true
    }
  }
  
  function uiLikePost(refresh = false) {
    likePostIcon = document.getElementById('like-post-trigger').querySelector('svg')
    likePostCount = document.getElementById('like-post-trigger').querySelector('span')
    if (isLikedPost()) {
      likePostIcon.classList.add('fill-red-500')
      if (!refresh) {
        likePostCount.innerHTML = parseInt(likePostCount.innerHTML) + 1
      }
    } else {
      likePostIcon.classList.remove('fill-red-500')
      if (!refresh) {
        likePostCount.innerHTML = parseInt(likePostCount.innerHTML) > 0 ? parseInt(likePostCount.innerHTML) - 1 : 0
      }
    }
  }
  
  function toggleLikePost() {
    likedPosts = JSON.parse(localStorage.getItem('likedPosts')) || []
    if (isLikedPost()) {
      result = fetch("{% url 'blog:post_unlike' post.slug %}", {
        method: 'GET'
      })
        .then((response) => response.ok)
        .then((ok) => {
          if (ok) {
            likedPosts.splice(likedPosts.indexOf('{{ post.slug }}'), 1)
            localStorage.setItem('likedPosts', JSON.stringify(likedPosts))
            uiLikePost()
          }
        })
    } else {
      result = fetch("{% url 'blog:post_like' post.slug %}", {
        method: 'GET'
      })
        .then((response) => response.ok)
        .then((ok) => {
          if (ok) {
            likedPosts.push('{{ post.slug }}')
            localStorage.setItem('likedPosts', JSON.stringify(likedPosts))
            uiLikePost()
          }
        })
    }
  }
  
  uiLikePost(true)
  likePostTrigger = document.getElementById('like-post-trigger')
  likePostTrigger.addEventListener('click', toggleLikePost)
  
  commentPostTrigger = document.getElementById('comment-post-trigger')
  // on click scroll to #comment-section
  commentPostTrigger.addEventListener('click', function () {
    commentSection = document.getElementById('comment-section')
    commentSection.scrollIntoView({
      behavior: 'smooth'
    })
  })