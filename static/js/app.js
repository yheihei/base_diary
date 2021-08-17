class starButton {
  constructor(csrftoken, postId, userId, starId=0) {
    this.csrftoken = csrftoken;
    this.postId = postId;
    this.userId = userId;
    this.starId = starId;
    this.element = document.querySelector(`.star.star--post-id-${postId}`);

    /**
     * 初期化
     */
     this.init = () => {
      if (this.starId) {
        // いいね済の場合
        this.element.textContent = 'いいね済';
        this.element.removeEventListener('click', this.addStar)
        this.element.addEventListener('click', this.removeStar)
      } else {
        // まだいいね!していない
        this.element.textContent = 'いいねする';
        this.element.removeEventListener('click', this.removeStar)
        this.element.addEventListener('click', this.addStar)
      }
    }

    /**
     * 通信中にいいね!ボタン押下不可にする
     */
    this.disabled = () => {
      this.element.classList.remove('star--enabled');
      this.element.classList.add('star--disabled');
    }

    /**
     * いいね!ボタン押下可能にする
     */
    this.enabled = () => {
      this.element.classList.remove('star--disabled');
      this.element.classList.add('star--enabled');
    }

    /**
     * 非同期通信でいいね!する
     */
    this.addStar = async () => {
      this.disabled();

      let response = await fetch('/api/stars/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': this.csrftoken,
          'Content-Type': 'application/json'
        },
        body:JSON.stringify({
            post: this.postId,
            user: this.userId
        })
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      if (response.status !== 201) {
        throw new Error(response.status);
      }
      const data = await response.json();
      this.starId = data['id']
      this.init();

      this.enabled();
    }

    /**
     * 非同期通信でいいね!を取り消す
     */
    this.removeStar = async () => {
      this.disabled();

      let response = await fetch(`/api/stars/${this.starId}`, {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': this.csrftoken,
          'Content-Type': 'application/json'
        }
      })
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      if (response.status !== 204) {
        throw new Error(response.status);
      }
      this.starId = 0;
      this.init();

      this.enabled();
    }
  }
}