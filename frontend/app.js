window.onload = function () {
  function assistantElement(msg) {
    // <div class="alert alert-info" role="alert">${msg}</div>
    let temp = document.createElement("div");
    temp.classList.add("alert");
    temp.classList.add("alert-info");
    temp.setAttribute("role", "alert");
    temp.innerText = msg;
    return temp;
  }

  function userElement(msg) {
    // <div class="alert alert-dark" role="alert">${msg}</div>
    let temp = document.createElement("div");
    temp.classList.add("alert");
    temp.classList.add("alert-dark");
    temp.setAttribute("role", "alert");
    temp.innerText = msg;
    return temp;
  }

  function appendMessage(msgs, msg) {
    msgs.push(msg);
  }

  const State = {
    CHOOSE_CONTRACT: 0,
    CONTRACT: 3,
    TIMELOCK: 1,
    ERC20: 2,
    CUSTOM: 4
  };

  const StateUrl = {
    CHOOSE_CONTRACT: "http://192.168.10.11:8080/converse/choose-contract",
    CONTRACT: "http://192.168.10.11:8080/test",
    TIMELOCK: "http://192.168.10.11:8080/converse/lock",
    ERC20: "http://192.168.10.11:8080/converse/erc20",
    CUSTOM: "http://192.168.10.11:8080/converse/code-gen",
  };

  var state = State.CHOOSE_CONTRACT;

  messages = [];

  var history = document.getElementById("messages");

  function updateHistory() {
    while (history.hasChildNodes()) {
      history.firstChild.remove();
    }
    messages.forEach((m) => {
      if (m.role == "assistant") {
        history.appendChild(assistantElement(m.content));
      }
      if (m.role == "user") {
        history.appendChild(userElement(m.content));
      }
    });
  }

  function converse() {
    var converseUrl;
    switch (state) {
      case State.CHOOSE_CONTRACT:
        converseUrl = StateUrl.CHOOSE_CONTRACT;
        break;
      case State.CONTRACT:
        converseUrl = StateUrl.CONTRACT;
        break;
      case State.TIMELOCK:
        converseUrl = StateUrl.TIMELOCK;
        break;
      case State.ERC20:
        converseUrl = StateUrl.ERC20;
        break;
        case State.CUSTOM:
          converseUrl = StateUrl.CUSTOM;
          break;
    }
    // function converseChooseContract() {
    fetch(converseUrl, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ messages }),
    })
      .then((response) => response.json())
      .then((response) => {
        console.log(JSON.stringify(response));
        appendMessage(messages, response);
        console.log(messages);

        if (response.contractType != undefined) {
          console.log(`got contract type: ${response.contractType}`);
          messages = [];

          switch (response.contractType) {
            case "erc20":
              state = State.ERC20;
              converse();
              break;
            case "time-lock":
              state = State.TIMELOCK;
              converse();
              break;
            case "custom":
              state = State.CUSTOM;
              converse();
              break;
            case null:
              state = State.CHOOSE_CONTRACT;
              // state = State.CONTRACT;
              converse();
              break;
          }
        }

        if (response.src != undefined) {
          messagesElement = document.getElementById("messages");
          userInputElement = document.getElementById("userinput");
          codeElement = document.getElementById("code");
          deployButtonElement = document.getElementById("deployBtn");
          issuesElement = document.getElementById("issues")

          messagesElement.classList.add("visually-hidden");
          userInputElement.classList.add("visually-hidden");
          codeElement.classList.remove("visually-hidden");
          codeElement.innerText = response.src;
          deployButtonElement.classList.remove("visually-hidden");
          if (state == State.CUSTOM) {
            issuesElement.classList.remove("visually-hidden")
            if (response.issues.length > 0) {
              issuesElement.innerText = response.issues
              issuesElement.classList.remove("alert-success")
              issuesElement.classList.add("alert-danger")
            } else {
              issuesElement.innerText = "No security issues identified"
              issuesElement.classList.remove("alert-danger")
              issuesElement.classList.add("alert-success")
            }
          }

          // hljs.initHighlightingOnLoad
          hljs.highlightAll();
        }

        updateHistory();
      });
  }

  function sendMessage() {
    if (messages.length == 0 || ele.value.length == 0) return;

    messages.push({ role: "user", content: ele.value });
    ele.value = "";
    updateHistory();
    converse();
  }
  const ele = document.getElementById("textbox");

  ele.addEventListener("keydown", function (e) {
    console.log;
    // Get the code of pressed key
    const keyCode = e.which || e.keyCode;

    // 13 represents the Enter key
    if (keyCode === 13 && !e.shiftKey) {
      // Don't generate a new line
      e.preventDefault();

      if (messages.length == 0) return;
      sendMessage();
    }
  });

  converse();
};
