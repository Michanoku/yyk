// Toggle SVG in Kanji view
var strokeToggle = "off";
var color = "black";

function toggleStrokes() {
  if (strokeToggle == "off" && color == "black") {
    document.getElementById("svgblack").style.display = "none";
    document.getElementById("svgblackstrokes").style.display = "block";
  strokeToggle = "on";
  }
  else if (strokeToggle == "on" && color == "black") {
    document.getElementById("svgblack").style.display = "block";
    document.getElementById("svgblackstrokes").style.display = "none";
    strokeToggle = "off";
  }
  else if (strokeToggle == "off" && color == "color") {
    document.getElementById("svgcolor").style.display = "none";
    document.getElementById("svgcolorstrokes").style.display = "block";
    strokeToggle = "on";
  }
  else if (strokeToggle == "on" && color == "color") {
    document.getElementById("svgcolor").style.display = "block";
    document.getElementById("svgcolorstrokes").style.display = "none";
    strokeToggle = "off";
  }
}

function toggleColor() {
  if (strokeToggle == "off" && color == "black") {
    document.getElementById("svgblack").style.display = "none";
    document.getElementById("svgcolor").style.display = "block";
    color = "color";
  }
  else if (strokeToggle == "on" && color == "black") {
    document.getElementById("svgblackstrokes").style.display = "none";
    document.getElementById("svgcolorstrokes").style.display = "block";
    color = "color";
  }
  else if (strokeToggle == "off" && color == "color") {
    document.getElementById("svgcolor").style.display = "none";
    document.getElementById("svgblack").style.display = "block";
    color = "black";
  }
  else if (strokeToggle == "on" && color == "color") {
    document.getElementById("svgcolorstrokes").style.display = "none";
    document.getElementById("svgblackstrokes").style.display = "block";
    color = "black";
  }
}

// Toggle Grade or JLPT in kanji view and vocabulary view
function toggleGrade() {
  document.getElementById("sorted_jlpt").style.display = "none";
  document.getElementById("sorted_kanjigrade").style.display = "block";
}

function toggleKanjiJlpt() {
  document.getElementById("sorted_kanjigrade").style.display = "none";
  document.getElementById("sorted_jlpt").style.display = "block";
}

function toggleHiragana() {
  document.getElementById("katakana-study").style.display = "none";
  document.getElementById("hiragana-study").style.display = "block";
}

function toggleKatakana() {
  document.getElementById("hiragana-study").style.display = "none";
  document.getElementById("katakana-study").style.display = "block";
}

function toggleStats() {
  document.getElementById("settings").style.display = "none";
  document.getElementById("statistics").style.display = "block";
}

function toggleSet() {
  document.getElementById("statistics").style.display = "none";
  document.getElementById("settings").style.display = "block";
}

function toggleVocabJlpt() {
  document.getElementById("sorted_kana").style.display = "none";
  document.getElementById("sorted_jlpt").style.display = "block";
}

function toggleKana() {
  document.getElementById("sorted_jlpt").style.display = "none";
  document.getElementById("sorted_kana").style.display = "block";
}

// Toggle Strokes, Grade or JLPT in radical view
function sortStrokes() {
  document.getElementById("sorted_grade").style.display = "none";
  document.getElementById("sorted_jlpt").style.display = "none";
  document.getElementById("sorted_strokes").style.display = "block";
}

function sortGrade() {
  document.getElementById("sorted_strokes").style.display = "none";
  document.getElementById("sorted_jlpt").style.display = "none";
  document.getElementById("sorted_grade").style.display = "block";
}

function sortJlpt() {
  document.getElementById("sorted_strokes").style.display = "none";
  document.getElementById("sorted_grade").style.display = "none";
  document.getElementById("sorted_jlpt").style.display = "block";
}