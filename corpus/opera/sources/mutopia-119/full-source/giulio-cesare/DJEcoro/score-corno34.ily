\score {
  \instrStaff \markup \instruments { 
    "Corno III. IV." \smaller \italic "ex D." }
  <<
    \keepWithTag #'(partBoth horn) \global
    \set Score.aDueText = ""
    \partcombine \includeNotes "corno3" \includeNotes "corno4"
  >>
  \header {
    opus = "Coro. Ritorni omai nel nostro core"
    breakbefore = #(break-before?) 
  }
  \layout { }
}
