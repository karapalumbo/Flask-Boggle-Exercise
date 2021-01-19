let count = 0;
let nonDuplicates = new Set();

$(".user-word").on("submit", async function (e) {
  e.preventDefault();

  const $msg = $(".msg");
  const $score = $(".score");
  const $word = $(".word");
  const form = $(".user-word");
  let highscore = $("#highscore");
  let userword = $(".word-container");
  let word = $word.val();
  let button = $(".submit");

  count++;

  if (word === "") {
    return;
  }

  const response = await axios.get("/check-word", {
    params: { word: word },
  });

  $msg.text("");
  $word.val("");

  if (response.data.result === "not-word") {
    $msg.append(`${word} is not a valid word.`);
  } else if (response.data.result === "not-on-board") {
    $msg.append(`${word} is not listed on the board.`);
  } else {
    let initialVal = parseInt($score.text());

    if (nonDuplicates.has(word)) {
      $msg.append(`${word} already found`);
    } else {
      $score.text((initialVal += word.length));
      userword.append(`<li>${word}</li>`);
      nonDuplicates.add(word);
      $msg.append(`${word} added.`);
    }
  }

  let timer = 20;
  if (count === 1) {
    let interval = setInterval(async function () {
      timer--;

      if (timer === 0) {
        clearInterval(interval);
        $("#timer").html("<h3>Game Over!</h3>");
        button.disabled = true;
        // form.hide();
        $msg.hide();

        const response = await axios.post("/user-score", {
          $score: parseInt($score.text()),
        });

        if (response.data.brokeRecord) {
          highscore.append(`New record: ${score}`);
        }
        return;
      } else {
        $("#time").text(timer);
      }
    }, 1000);
  }
});
