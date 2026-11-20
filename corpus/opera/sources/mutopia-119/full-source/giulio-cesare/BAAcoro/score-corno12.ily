\score {
  \instrStaff \markup \instruments { "Corno I.II." " in A." } <<
    \scoreInit
    \keepWithTag #'(partBoth horn-A) \global
    \new Voice { \voiceOne \includeNotes "corno1" }
    \new Voice { \voiceTwo \includeNotes "corno2" }
    \new Voice { \oneVoice \includeNotes "corno12-rests" }
  >>
  \header { 
    piece = "Atto Primo, Scena I."
    opus = "Coro. Viva il nostre Alcide"
    breakbefore = #(break-before?)
  }
  \layout { }
}
