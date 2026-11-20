\score {
  \instrStaff \markup \instruments { "Corno III.IV." "in D." } <<
    \keepWithTag #'(partBoth horn-D) \global
    \new Voice {\voiceOne \includeNotes "corno3" }
    \new Voice {\voiceTwo \includeNotes "corno4" }
    \new Voice {\oneVoice \includeNotes "corno34-rests" }
  >>
  \header { 
    piece = "Atto Primo, Scena I."
    opus = "Coro. Viva il nostre Alcide"
    breakbefore = #(break-before?)
  }
  \layout { }
}
