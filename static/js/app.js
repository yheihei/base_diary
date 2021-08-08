class starButton {
  constructor(csrftoken, postId, userId, starId=0) {
    this.csrftoken = csrftoken;
    this.postId = postId;
    this.userId = userId;
    this.starId = starId;
    this.element = document.querySelector(`.star.star--post-id-${postId}`);

    this.isFetching = false;

    /**
     * 通信中にいいね!ボタン押下不可にする
     */
    this.disabled = () => {
      this.element.style.pointerEvents = 'none';
      this.isFetching = true;
    }

    /**
     * いいね!ボタン押下可能にする
     */
    this.enabled = () => {
      this.element.style.pointerEvents = '';
      this.isFetching = false;
    }

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
     * 非同期通信でいいね!する
     */
    this.addStar = async () => {
      // 連打対策
      if (this.isFetching) {
        console.log('通信中のためskip');
        return;
      }
      this.disabled();

      let response = await fetch("/api/stars/", {
        method: "POST",
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
      console.log("status=" + response.status);
      if (response.status !== 201) {
        throw new Error(response.status);
      }
      const data = await response.json();
      this.starId = data['id']
      console.log(data);
      this.init();
      this.enabled();
    }

    /**
     * 非同期通信でいいね!を取り消す
     */
    this.removeStar = async () => {
      // 連打対策
      if (this.isFetching) {
        console.log('通信中のためskip');
        return;
      }
      this.disabled();

      let response = await fetch(`/api/stars/${this.starId}`, {
        method: "DELETE",
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