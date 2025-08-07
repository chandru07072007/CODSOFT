const questions = [
  {
    question: "Which of these is NOT a pillar of OOPS in Java?",
    options: ["Encapsulation", "Inheritance", "Compilation", "Abstraction"],
    answer: 2
  },
  {
    question: "Which access modifier restricts the visibility of a class member to only within the same class?",
    options: ["public", "private", "protected", "package-private"],
    answer: 1
  },
  {
    question: `Given the following code, what will be the output?\n\nclass A {\n  void show() { System.out.print("A"); }\n}\nclass B extends A {\n  void show() { System.out.print("B"); }\n}\npublic class Test {\n  public static void main(String[] args) {\n    A obj = new B();\n    obj.show();\n  }\n}`,
    options: ["A", "B", "AB", "Error"],
    answer: 1
  },
  {
    question: "Which of the following best describes encapsulation?",
    options: [
      "Hiding the implementation and exposing functionality",
      "Using methods with the same name",
      "Deriving classes from other classes",
      "Overriding parent class methods"
    ],
    answer: 0
  },
  {
    question: "What is the purpose of the ‘final’ keyword in Java?",
    options: ["Prevent inheritance", "Allow overriding", "Hide data", "Enable overloading"],
    answer: 0
  },
  {
    question: "Which method signature is valid for method overloading in Java?",
    options: [
      "void setValue(int a) and void setValue(int b)",
      "void setValue(int a) and void setValue(int a, int b)",
      "Only one method named setValue allowed",
      "Overloading is not supported"
    ],
    answer: 1
  },
  {
    question: "How can a class in Java extend only one class but implement multiple interfaces?",
    options: [
      "By using multiple inheritance",
      "Interfaces do not support implementation",
      "Java supports single inheritance for classes and multiple for interfaces",
      "Classes cannot implement interfaces"
    ],
    answer: 2
  },
  {
    question: "Which of the following statements about abstract classes is TRUE?",
    options: [
      "Abstract class can’t have any methods",
      "Abstract class must contain only abstract methods",
      "Abstract class can have both abstract and concrete methods",
      "Abstract class must be private"
    ],
    answer: 2
  },
  {
    question: "When is dynamic polymorphism determined in Java?",
    options: ["Compile time", "Run time", "Debug time", "None of the above"],
    answer: 1
  },
  {
    question: `What will be the output of the following code?\n\nabstract class Base { abstract void run(); }\nclass Derived extends Base {\n  void run() { System.out.print("Running"); }\n}\npublic class Main {\n  public static void main(String[] args) {\n    Base b = new Derived();\n    b.run();\n  }\n}`,
    options: ["Error", "Running", "Compiles with warning", "No output"],
    answer: 1
  }
];

const totalQuestions = questions.length;
let currentQ = 0, score = 0, selected = null, lock = false;
let timerInterval = null;
const TIMER_DURATION = 30;
let timeLeft = TIMER_DURATION;

function byId(id) { return document.getElementById(id); }

function loadQuestion(idx) {
  lock = false;
  timeLeft = TIMER_DURATION;
  byId("timer").textContent = timeLeft;
  byId("nextBtn").disabled = true;
  byId("question-number").innerText = `Question ${idx+1}/${totalQuestions}`;
  byId("question").innerText = questions[idx].question;
  const optionsEl = byId("options");
  optionsEl.innerHTML = "";
  questions[idx].options.forEach((opt, i) => {
    const btn = document.createElement("button");
    btn.innerText = opt;
    btn.onclick = () => selectOption(btn, i);
    optionsEl.appendChild(btn);
  });
  updateProgress();
  startTimer();
}
function startTimer() {
  clearInterval(timerInterval);
  timerInterval = setInterval(() => {
    timeLeft--;
    byId("timer").textContent = timeLeft;
    if (timeLeft <= 0) {
      clearInterval(timerInterval);
      lock = true;
      showCorrect();
      byId("nextBtn").disabled = false;
    }
  }, 1000);
}
function updateProgress() {
  byId('progress').style.width = ((currentQ+1) * 100 / totalQuestions) + '%';
  byId('score').textContent = score;
}
function selectOption(btn, idx) {
  if (lock) return;
  const buttons = document.querySelectorAll('.options button');
  buttons.forEach(b => b.classList.remove("selected","correct","incorrect"));
  btn.classList.add("selected");
  selected = idx;
  byId("nextBtn").disabled = false;
}
function showCorrect() {
  lock = true;
  const buttons = document.querySelectorAll('.options button');
  buttons.forEach((btn, idx) => {
    btn.classList.remove("selected");
    if(idx === questions[currentQ].answer) btn.classList.add("correct");
    else if(idx === selected) btn.classList.add("incorrect");
    btn.disabled = true;
  });
  byId("nextBtn").disabled = false;
}
byId("nextBtn").onclick = function() {
  clearInterval(timerInterval);
  if(selected === questions[currentQ].answer) score++;
  showCorrect();
  setTimeout(() => {
    fadeOutIn(nextQuestion);
  }, 700);
};
function fadeOutIn(callback) {
  const card = byId("questionCard");
  card.style.opacity = 0;
  card.style.transform = "translateY(30px)";
  setTimeout(() => {
    callback();
    card.style.opacity = 1;
    card.style.transform = "translateY(0)";
  }, 250);
}
function nextQuestion() {
  selected = null;
  currentQ++;
  if(currentQ === totalQuestions) {
    finishQuiz();
  } else {
    loadQuestion(currentQ);
  }
}
function finishQuiz() {
  byId("question-number").style.display = 'none';
  byId("question").style.display = 'none';
  byId("options").style.display = 'none';
  byId("nextBtn").style.display = 'none';
  byId("progress").style.width = '100%';
  byId("resultSection").style.display = 'block';
  byId("finalScore").innerText = score;
}
byId("restartBtn").onclick = function() {
  currentQ = 0; score = 0; selected = null;
  byId("question-number").style.display = '';
  byId("question").style.display = '';
  byId("options").style.display = '';
  byId("nextBtn").style.display = '';
  byId("resultSection").style.display = 'none';
  loadQuestion(currentQ);
};
// Initialize
loadQuestion(currentQ);
