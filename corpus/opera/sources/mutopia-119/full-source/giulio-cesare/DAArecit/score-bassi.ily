\score {
  \new OrchestraStaffGroup <<
    \smallerRecitStaff <<
      \keepWithTag #'recit  \global
      \achilla \includeNotes #"achilla"
    >> \includeLyrics #"achilla-lyrics"
    \instrStaff \markup "" <<
      \scoreInit
      \keepWithTag #'partDown \global
      \clef bass
      \includeNotes #"bassi"
    >>
  >>
  \header {
    piece = "Atto Terzo, Scena I."
    opus = "Recitativo."
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
