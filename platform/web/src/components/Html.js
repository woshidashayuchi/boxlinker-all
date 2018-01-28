import React, { PropTypes } from 'react';
// import { analytics } from '../config';

function Html({ title, description, bootstrapCss, style, script, children, state }) {
  return (
    <html className="no-js" lang="">
      <head>
        <meta charSet="utf-8" />
        <meta httpEquiv="x-ua-compatible" content="ie=edge" />
        <title>{title}</title>
        <meta name="description" content={description} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="apple-touch-icon" href="apple-touch-icon.png" />
        <link rel="stylesheet" href="/icomoon/style.css"/>
        <link rel="stylesheet" href={bootstrapCss} />
        <style id="css" dangerouslySetInnerHTML={{ __html: style }} />
        <script id = "script"></script>
      </head>
      <body>
        <div id="app" dangerouslySetInnerHTML={{ __html: children }} />
        {script && (
          <script
            id="source"
            src={script}
            data-initial-state={JSON.stringify(state)}
          />
        )}
        {/*<script src='//kefu.easemob.com/webim/easemob.js?tenantId=30589&hide=false&sat=false' async='async'></script>*/}
        {/*<script src="http://www.sobot.com/chat/pc/pc.min.js?sysNum=91464991599947c5a59b66e9d2c05ac6" id="zhichiload" ></script>*/}
      </body>
    </html>
  );
}

Html.propTypes = {
  title: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  style: PropTypes.string.isRequired,
  script: PropTypes.string,
  children: PropTypes.string,
  state: PropTypes.object.isRequired,
};

export default Html;
