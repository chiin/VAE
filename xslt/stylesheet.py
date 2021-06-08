import datetime

COPYRIGHT_NOTICE = "© Copyright XXXX The Legislative Council"


def get_copyright_notice(copyright_notice: str = COPYRIGHT_NOTICE) -> str:
    current_year_str = str(datetime.datetime.now().year)
    return copyright_notice.replace("XXXX", current_year_str)

XSL_ADD_WORD_COUNT_BY_SPEECH = '''

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0"
    version="1.0">
    <xsl:output method="xml"/>

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="name">
        <name key="{@key}">
            <xsl:value-of select="."/>
        </name>

        <measure>
            <name>
                <xsl:value-of select="@key"/>
            </name>
            <wordcount>
                <xsl:value-of select=
                " string-length(normalize-space(..))
                -
                string-length(translate(normalize-space(..),' ',''))+1
                "/>
            </wordcount>
        </measure>
    </xsl:template>
</xsl:stylesheet>

'''


XSL_SUM_WORD_COUNT_BY_NAME = '''

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output omit-xml-declaration="yes" indent="yes"/>
 
    <xsl:key name="kspeaker" match="measure" use="name"/>
    <xsl:template match="measure[
        generate-id() = generate-id(key('kspeaker',name)[1])
        ]">
        <totalwordcount>
            <xsl:attribute name="name">
                <xsl:copy-of select="name"/>
            </xsl:attribute>
            <xsl:attribute name="value">
                <xsl:value-of select="sum(key('kspeaker',name)/wordcount)"/>
            </xsl:attribute>
        </totalwordcount>
    </xsl:template>

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>

'''

XSL_ADD_TABLE_CONVERT_TO_HTML = '''
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" indent="yes"/>

    <xsl:template match="/">
        <html>
            <head>
                <title> Word count </title>
                <xsl:apply-templates mode="table"/>
            </head>
            <body>
                <xsl:apply-templates mode="all"/>
                <xsl:text>''' + get_copyright_notice() + '''</xsl:text>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="body" mode="table">
        <table width="400" border="1">
            <tr bgcolor="#cccccc">
                <td>SPEAKER</td>
                <td>NUMBER OF WORDS</td>
            </tr>
            <xsl:for-each select="//totalwordcount">
                <tr>
                    <td>
                        <xsl:value-of select="@name"/>
                    </td>
                    <td>
                        <xsl:value-of select="@value"/>
                    </td>
                </tr>
            </xsl:for-each>
        </table>
    </xsl:template>
    
    <xsl:template match="measure" mode="all">
    </xsl:template>

    <xsl:template match="name" mode="all">
        <b>
            <xsl:copy-of select="."/>
        </b>
    </xsl:template>
    
    <xsl:template match="p" mode="all">
        <p>
            <xsl:apply-templates mode="all"/>
        </p>
    </xsl:template>
</xsl:stylesheet>

'''