\score {
  \new OrchestraStaffGroup <<
    \smallerRecitStaff <<
      \keepWithTag #'recit \global
      \cleopatra \includeNotes #"cleopatra"
    >> \includeLyrics #"cleopatra-lyrics"
    \instrStaff \markup "" <<
      \scoreInit
      \keepWithTag #'partDown \global
      \clef bass \includeNotes #"bassi"
    >>
  >>
  \header {
    piece = "Scena III."
    opus = "Recitativo."
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
