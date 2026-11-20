\version "2.9.2"
#(use-modules (ice-9 optargs))
#(ly:set-option 'point-and-click #f)

\include "common/loop-guile.ily"

%% Custom page breaking scheme
%% Commands for including and defining page layout tweaks
\include "common/book-page-layout.ily"

%% Custom figured bass
\include "common/figured-bass.ily"

%% Misc commands
%% Shortcuts for including notes, lyrics, figures
%% Shortcuts for defining staves
\include "common/commands.ily"

%% Tempo markups and rehearsal marks
%% Da Capo markups and rehearsal marks
%% Various markups and titling commands
\include "common/marks.ily"

%% Include tweak file, if exists.
\includePageLayoutFile

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Default page layout
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Staff size
#(set-global-staff-size 14)
%% Paper size
#(set-default-paper-size (if (*use-letter-paper*)
                             "letter"
                             "a4"))

\paper {
  %% Opera custom titling
  \include "common/titling.ily"
  
  page-top-space = #(* 5 mm)
  left-margin = 15\mm
  right-margin = 15\mm
  #(define line-width (- paper-width (* 30 mm)))

  #(define-public book-title (marked-up-title 'operaBookTitleMarkup))
  #(define-public score-title (marked-up-title 'operaScoreTitleMarkup))
  
  #(define make-header (marked-up-headfoot 'operaOddHeaderMarkup 
                        'operaEvenHeaderMarkup))
  #(define make-footer (marked-up-headfoot 'operaOddFooterMarkup 
                        'operaEvenFooterMarkup))
}

\layout {
  noindent = 0\mm
  smallindent = 5\mm
  largeindent = 25\mm
  indent = \largeindent

  \context {
    \Score
    \remove "Mark_engraver" 
    \override BarNumber #'padding = #2 
    \override InstrumentName #'space-alist = #'((left-edge extra-space . 2.0))
    \accepts "OrchestraStaffGroup"
  }
  \context {
    \StaffGroup
    \name OrchestraStaffGroup
    \description "Like StaffGroup, but without spanbar"
    \remove "Span_bar_engraver"
    \accepts "InstrumentStaffGroup"
  }
  \context {
    \StaffGroup
    \name InstrumentStaffGroup
    \description "Like StaffGroup, but without brackets"
    \remove "System_start_delimiter_engraver"
  }
  \context {
    \Staff
    \consists "Mark_engraver"
  }
  \context {
    \Lyrics
    minimumVerticalExtent = #'(-0 . 0)
  }
}
