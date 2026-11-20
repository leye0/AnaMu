\score {
  \new OrchestraStaffGroup <<
    \smallerRecitStaff <<
      \override Score.VerticalAxisGroup #'remove-first = ##t
      \keepWithTag #'partUp \global
      \cleopatra \includeNotes #"cleopatra" 
    >> \includeLyrics #"cleopatra-lyrics"
    \instrStaff \markup "" <<
      \scoreInit
      \keepWithTag #'partDown \global
      \clef bass \includeNotes #"bassi"
      \includeFigures #"figures"
    >>
  >>
  \header {
    piece = "Scena VII."
    opus = "Recit. Cleopatra: Voi, che mie fide ancelle"
    breakbefore = #(break-before?) 
  }
  \layout {
    indent = \smallindent
    \context {
      \RemoveEmptyStaffContext
      \consists "Mark_engraver" 
    } 
  }
}
