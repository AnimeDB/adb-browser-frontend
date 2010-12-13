# -*- coding: utf-8 -*-

import re
import urlparse
import urllib2

from pyparsing import *


class PostParser(object):
    url_regex = r'''(?xi)
        \b
        (                           # Capture 1: entire matched URL
          (?:
            [a-z][\w-]+:                # URL protocol and colon
            (?:
              /{1,3}                        # 1-3 slashes
              #|                             #   or
              #[a-z0-9%]                     # Single letter or digit or '%'
                                            # (Trying not to match e.g. "URI::Escape")
            )
            |                           #   or
            www\d{0,3}[.]               # "www.", "www1.", "www2." … "www999."
            |                           #   or
            [a-z0-9.\-]+[.][a-z]{2,4}/  # looks like domain name followed by a slash
          )
          (?:                           # One or more:
            [^][\s()^<>]+                      # Run of non-space, non-()<>
            |                               #   or
            \(([^\s()<>]+|(\([^\s()<>]+\)))*\)  # balanced parens, up to 2 levels
          )+
          (?:                           # End with:
            \(([^\s()<>]+|(\([^\s()<>]+\)))*\)  # balanced parens, up to 2 levels
            |                                   #   or
            [^\s`!()\[\]{};:'".,<>?«»“”‘’]        # not a space or one of these punct chars
          )
        )'''
        
    groups = {
        'wikipedia': r'^http://(?:[a-z]{2,3}.)?wikipedia.org/',
        'megavideo': r'^http://(?:www.)?megavideo.com/',
    }
    
    def __init__(self):
        pass
    
    def makeBBTags(self, tag, strip=True):
        if isinstance(tag,basestring):
            tag = Keyword(tag, caseless=True)

        value = quotedString.copy()
        
        if strip:
            value = value.setParseAction(removeQuotes)

        attribute = value | Word(printables.replace(']', ''))
        
        attr = Literal("=")
        
        if strip:
            attr = Suppress(attr)
            o = Suppress("[")
            c = Suppress("[/")
            e = Suppress("]")
        else:
            o = Literal("[")
            c = Literal("[/")
            e = Literal("]")
        
        openTag = o + tag + Optional(attr + attribute) + e
        closeTag = Combine(c + tag + e)
        
        if strip:
            closeTag = Suppress(closeTag)

        return openTag, closeTag
    
    def makeTagParser(self, tag):
        start, end = self.makeBBTags(tag)
        return start + SkipTo(end) + end
    
    def normalize_url(self, url):
        return urlparse.urlunsplit(urlparse.urlsplit(url))
    
    def filter(self, url):
        ignored = (
            r'http://(www\.)?animedb\.tv',
            r'http://Nessuno',
        )
        
        for r in ignored:
            if re.match(r, url):
                return True
        else:
            return False
    
    def isresource(self, url):
        components = urlparse.urlsplit(url)
        domain =  '.'.join(components.netloc.split('.')[-2:])
        
        resources = set(('duckload.com', 'megavideo.com'))
        return domain in resources
    
    def userparser(self, text):
        anyBBTag, anyBBClose = self.makeBBTags(Word(alphas), strip=False)

        by = (Keyword('by', caseless=True) | Keyword('Upper:', caseless=True)) + Optional(anyBBClose)
        username = (
            OneOrMore(anyBBTag) + SkipTo(anyBBClose).setResultsName("username").leaveWhitespace() + anyBBClose
        ) | (
            OneOrMore(Word(printables.replace('\n', ''), ).leaveWhitespace().setResultsName("username"))
        )
        
        import pprint
        result = []
        for tokens, start, end in (by + username).scanString(text):
            print tokens
            off = sum([len(tok) for tok in tokens if tok != tokens.username])
            username = self.striptags(tokens.username)
            result.append([username, start, end])
        
        pprint.pprint(result)
        
        return result
    
    def stripHTMLTag(self, tag, strip_content=False, html=True):
        if html:
            start, end = makeHTMLTags(tag)
        else:
            start, end = self.makeBBTags(tag)

        if strip_content:
            parser = start + SkipTo(end) + end
        else:
            parser = start | end

        parser.setParseAction(replaceWith(""))
        return parser


    def stripBBTag(self, tag, strip_content=False):
        return self.stripHTMLTag(tag, strip_content, False)
    

    def striptags(self, text):
        comments = htmlComment
        comments.setParseAction(replaceWith(""))
        anyhtmltag = self.stripHTMLTag('script', True) | self.stripHTMLTag(Word(alphas,alphanums+":_"))

        content = self.stripBBTag('contenuto', True)
        imgs = self.stripBBTag('img', True)
        anybbtag = self.stripBBTag((Literal('coloruguale#') + Word(hexnums)) | Word(alphas))

        bbtags = content | imgs | anybbtag
        htmltags = comments | commonHTMLEntity | anyhtmltag

        stripper = (bbtags | htmltags).transformString

        return re.sub(r'\n+', '\n', re.sub(r'[\t ]+', ' ', stripper(text))).strip()
    
    def parse(self, text):
        all_urls = self.urls(text)
        ignored = set(filter(self.filter, all_urls))
        
        result = {
            'Contenuto': set(),
            'Immagine': set(),
            'Risorsa': set(),
            'Ignorato': ignored,
            'errors': set(),
            'undetected': set(),
            'Altro': all_urls.copy() - ignored,
        }
        
        contentParser = self.makeTagParser('contenuto')
        
        for tokens, start, end in contentParser.scanString(text):
            url = tokens[1]
            if url not in all_urls:
                print "Undetected", result['undetected']#.add((url, tokens[2]))
                continue
            
            result['Altro'].discard(url)
            result['Contenuto'].add((url, ''))
            
        imgParser = self.makeTagParser('img')
        
        for tokens, start, end in imgParser.scanString(text):
            url = tokens[1]
            if url not in all_urls:
                print "Undetected", result['undetected']#.add((url, tokens[2]))
                continue
            
            if url not in result['Ignorato']:
                result['Altro'].discard(url)
                result['Immagine'].add((url, ''))
        
        urlParser = self.makeTagParser('url') | self.makeTagParser('v')
        
        for tokens, start, end in urlParser.scanString(text):
            url = tokens[1]
            
            try:
                urltext = tokens[2]
            except IndexError:
                print "No url text", tokens
                urltext = ''
            
            if url not in all_urls:
                print "Undetected", result['undetected']#.add((url, tokens[2]))
                continue
            
            if url not in result['Ignorato']:
                result['Altro'].discard(url)
                
                if self.isresource(url):
                    result['Risorsa'].add((url, urltext))
                else:
                    result['Altro'].add((url, urltext))
            else:
                result['Ignorato'].discard(url)
                result['Ignorato'].add((url, urltext))
                
                # Search for URLs
                urls = set([self.normalize_url(u[0]) for u in re.findall(self.url_regex, urltext)])

                for url in urls:
                    result['Immagine'].discard((url, ''))
                    result['Ignorato'].add((url, ''))
        
        for key, urls in result.iteritems():
            if key in ('Ignorato', 'errors', 'undetected'):
                continue
            
            for url, title in urls.copy():
                class HeadRequest(urllib2.Request):
                    def get_method(self):
                        return "HEAD"
                
                req = HeadRequest(url.encode('utf-8'))
                req.add_header('User-Agent', 'AnimeDB')
                
                try:
                    pass #urllib2.urlopen(req)
                except Exception as e:
                    result[key].discard((url, title))
                    result['errors'].add((url, title, str(e), key))
        
        # Normalize dict
        normalized = []
        
        for key, urls in result.iteritems():
            for url in urls:
                address = url[0]
                
                res = [address, url[1]]
                
                if key == 'errors':
                    res += url[3], url[2]
                elif key == 'Ignorato':
                    res += key, None
                elif key == 'Altro':
                    res += key, None
                else:
                    res += key, False
                
                normalized.append(res)
                
        
        normalized.sort(key=lambda u: u[2])
        
        return result, normalized, self.userparser(text)
        
    
    def urls(self, text, plain=True):
        urls = set([self.normalize_url(u[0]) for u in re.findall(self.url_regex, text)])
        
        if plain:
            return urls
        
        groups = {}
        
        for url in urls:
            matched = False
            for group, pattern in self.groups.iteritems():
                if re.match(pattern, url):
                    matched = True
                    groups.setdefault(group, set()).add(url)
            if not matched:
                groups.setdefault('other', set()).add(url)
        
        return groups
