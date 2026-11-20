\version "2.9.7"
#(use-modules (ice-9 optargs))
#(ly:set-option 'point-and-click #f)

%% Custom figured bass
%%\include "../common/figured-bass.ily"

%% Misc commands
%% Shortcuts for including notes, lyrics, figures
%% Shortcuts for defining staves
\include "../common/commands.ily"

%% Tempo markups and rehearsal marks
%% Da Capo markups and rehearsal marks
%% Various markups and titling commands
\include "../common/marks.ily"

includePartScore = 
#(define-music-function (parser location score-id part-name) (string? string?)
  (parameterize ((*current-piece* (string-append "../" score-id)))
   (ly:parser-parse-string (ly:clone-parser parser) 
                       (string-append "\\include \"" 
                        (*current-piece*) "/score-" part-name ".ily\""))
   (make-music 'SequentialMusic 'void #t)))

#(define-markup-command (piece paper props arg) (markup?)
  (interpret-markup paper props 
   (markup #:fill-line (#:fontsize 3 arg))))

#(define-markup-command (opus paper props arg) (markup?)
  (interpret-markup paper props 
   (markup #:fill-line (#:fontsize 2 arg #:null))))

%% Staff size
#(set-global-staff-size 18)

\paper {
  page-top-space = #(* 5 mm)
  left-margin = 20\mm
  right-margin = 20\mm
  #(define line-width (- paper-width (* 40 mm)))
  print-page-number = ##t
  #(define page-breaking ly:page-turn-breaking)

  bookTitleMarkup = \markup \override #'(baseline-skip . 6) \column {
    \fill-line { \when-property #'header:composer
                 \column { \vspace #8
                           \fill-line { \fontsize #8 \italic \fromproperty #'header:composer }
                         \vspace #4 } }
    \fill-line { \when-property #'header:title
                 \column { \vspace #4
                           \fill-line { \fontsize #10 \fromproperty #'header:title }
                           \vspace #3
                           \fill-line { \fontsize #6 \fromproperty #'header:subtitle }
                         \vspace #4 } }
    \fill-line { \when-property #'header:title
                 \column { \vspace #8
                           \when-property #'header:instrument
                           \fill-line { \fontsize #6 \fromproperty #'header:instrument }
                         \vspace #4 } }
    \fill-line { \when-property #'header:edition
                 \column { \vspace #2
                           \fill-line { \fontsize #3 \fromproperty #'header:edition }
                           \vspace #10
                         }}
  }
  scoreTitleMarkup = \markup \column {
    \fill-line { \when-property #'header:piece
                 \piece \fromproperty #'header:piece 
               }
    \fill-line { \when-property #'header:opus
                 \opus \fromproperty #'header:opus 
               }
  }
  oddFooterMarkup = \markup {
  \column {
    \fill-line {
      % put copyright only on pagenr. 1 
      \on-the-fly #(lambda (layout props arg)
		    (if (= 1 (chain-assoc-get 'page:page-number props   -1))
		     (interpret-markup layout props arg)
		     empty-stencil))
      \fromproperty #'header:longcopyright
    }
    \fill-line {
      % put tagline only on last page
      \on-the-fly #(lambda (layout props arg)
		    (if (chain-assoc-get 'page:last?  props #f)
		     (interpret-markup layout props arg)
		     empty-stencil))
      \fromproperty #'header:tagline
    }
  }
}
}

\layout {
  noindent = 0\mm
  smallindent = 10\mm
  largeindent = 25\mm
  indent = \largeindent

  \context {
    \Score
    \remove "Mark_engraver"
    skipBars = ##t
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
    \description "Like StaffGroup, but withut brackets"
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

\header {
  maintainer = "Nicolas Sceaux"
  title = "GIULIO CESARE"
  subtitle = "IN EGITTO"
  composer = "George Frideric Haendel"
  edition = \markup \center-align {
    \line { From the Deutsche Händelgesellschaft Edition }
    \line { Edited by Frideric Chrysander }}
  copyright = \markup \line { Copyright © 2005-2006 \maintainer }
  longcopyright = \markup \center-align {
    \line { \copyright \hspace #-1 . }
    \line { Licensed under the Creative Commons Attribution 2.5 License }
  }

  instrument = "Viola."
  copyright = \markup \line { Copyright © 2005-2006 \maintainer }
  tagline = \markup { 
    \override #'(box-padding . 1.0) \override #'(baseline-skip . 2.7)
    \box \center-align {
      \small \line {
        \copyright
        \with-url #"http://nicolas.sceaux.free.fr"
        \teeny "<nicolas.sceaux.free.fr>"
        \hspace #-1 .
        Typeset using \with-url #"http://www.LilyPond.org" 
        \line { \teeny www. \hspace #-1.0 LilyPond \hspace #-1.0 \teeny .org }
        #(ly:export (string-append "version " (lilypond-version))) \hspace #-1 .
      }
      \small \line { 
        Sheet music from \with-url #"http://www.MutopiaProject.org"
        \line { \teeny www. \hspace #-1.0 MutopiaProject \hspace #-1.0 
                \teeny .org \hspace #0.5 }
        - \hspace #0.5 \italic Free to download, with the \italic freedom
        to distribute, modify and perform. } 
      \teeny \line { 
        Licensed under the Creative Commons Attributio 2.5 License, 
        for details see: \hspace #-0.5 
        \with-url #"http://creativecommons.org/licenses/by/2.5" 
        http://creativecommons.org/licenses/by/2.5 }
    }
  }
}


\score {
  { 
    \noPageBreak s4 
 }
  \layout {
    \context {
      \Staff
      \remove Time_signature_engraver
      \remove Key_engraver
      \remove Clef_engraver
      \remove Staff_symbol_engraver
    }
  }
}
\markup \null