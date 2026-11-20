\score {
  \instrStaff \markup \instruments { 
    "Corno I. II." \smaller \italic "ex G." }
  <<
    \keepWithTag #'(partBoth horn) \global
    \set Score.aDueText = ""
    \partcombine \includeNotes "corno1" \includeNotes "corno2"
  >>
  \header {
    opus = "Coro. Ritorni omai nel nostro core"
    breakbefore = #(break-before?) 
  }
  \layout { }
}
