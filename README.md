Webbriktlinjer till ODT/PDF
===========================

English summary: Script to generate PDF/ODT version of guidelines for public sector websites.


Detta script skapar ett HTML-dokument formaterat för utskrift och använder Open
Office eller motsvarande för att konvertera dokumentet till ODT. Efter
konvertering till ODT är det möjligt att öppna dokumentet i OpenOffice, göra
justeringar och spara som PDF eller annat format.

För att köra scriptet behövs en installation av programspråket Python och
modulerna requests och lxml.

Filen template.html innehåller stomme till dokumentet och de stilmallsregler
som används för sidbrytning mm.

Detta är en första version och ska betraktas mer som ett hack.


Vill du bidra?
--------------

Klona gärna detta repo och pusha ändringar så ska jag försöka föra in dem.



Licens
------

Öppen källkod: MIT-licensen

Copyright (c) 2012 Peter Krantz

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
