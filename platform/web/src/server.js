/**
 * React Starter Kit (https://www.reactstarterkit.com/)
 *
 * Copyright © 2014-2016 Kriasoft, LLC. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.txt file in the root directory of this source tree.
 */

import 'babel-polyfill';
import path from 'path';
import express from 'express';
import cookieParser from 'cookie-parser';
import bodyParser from 'body-parser';
import React from 'react';
import ReactDOM from 'react-dom/server';
import Html from './components/Html';
import { ErrorPage } from './routes/error/ErrorPage';
import errorPageStyle from './routes/error/ErrorPage.css';
import UniversalRouter from 'universal-router';
import PrettyError from 'pretty-error';
import createHistory from './core/createHistory'
import configureStore from './store/configureStore'
import routes from './routes';
import assets from './assets'; // eslint-disable-line import/no-unresolved
import { setRuntimeVariable } from './actions/runtime';
import { fetchUserInfo } from './actions/users'
import {toggleSidebarAction,onChangeSidebarActiveAction} from './actions/toggleSidebar'
const port = process.env.PORT || 3000;
const app = express();

//
// Tell any CSS tooling (such as Material UI) to use all vendor prefixes if the
// user agent is not known.
// -----------------------------------------------------------------------------
global.navigator = global.navigator || {};
global.navigator.userAgent = global.navigator.userAgent || 'all';

//
// Register Node.js middleware
// -----------------------------------------------------------------------------
app.use(express.static(path.join(__dirname, 'public')));
app.use(cookieParser());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.get('*', async (req, res, next) => {

  const history = createHistory(req.url);
  // let currentLocation = history.getCurrentLocation();
  let sent = false;
  const removeHistoryListener = history.listen(location => {
    const newUrl = `${location.pathname}${location.search}`;
    if (req.originalUrl !== newUrl) {
      // console.log(`R ${req.originalUrl} -> ${newUrl}`); // eslint-disable-line no-console
      if (!sent) {
        res.redirect(303, newUrl);
        sent = true;
        next();
      } else {
        console.error(`${req.path}: Already sent!`); // eslint-disable-line no-console
      }
    }
  });

  try {
    const store = configureStore({}, {
      isSidebarOpen: true,
      cookie: req.cookies,
      history,
    });
    const token = req.cookies["_at"];
    if ((!token||token == 'null') && req.path != '/login' && req.path != '/signUp') {
      res.redirect('/login')
      return;
    }
    store.dispatch(setRuntimeVariable({
      name: 'initialNow',
      value: Date.now(),
    }));
    store.dispatch(toggleSidebarAction(req.cookies["isSidebarOpen"] == "true"||true));
    store.dispatch(onChangeSidebarActiveAction(req.cookies["sidebarActive"]||"/"));
    if (!!token)
      await store.dispatch(fetchUserInfo(token,process.env.NODE_ENV == 'development'));

    let css = [];
    let statusCode = 200;
    const data = { title: '', description: '', style: '', bootstrapCss:assets.main.css, script: assets.main.js, children: '' };

    await UniversalRouter.resolve(routes, {
      path: req.path,
      query: req.query,
      context: {
        store: store,
        createHref: history.createHref,
        insertCss: (...styles) => {
          styles.forEach(style => css.push(style._getCss())); // eslint-disable-line no-underscore-dangle, max-len
        },
        setTitle: value => (data.title = value),
        // setMeta: (key, value) => (data[key] = value),
        pathname: req.path,
      },
      render(component, status = 200) {
        css = [];
        statusCode = status;
        data.children = ReactDOM.renderToString(component);
        data.style = css.join('');
        data.state = store.getState();
        return true;
      },
    });
    if (!sent) {
      const html = ReactDOM.renderToStaticMarkup(<Html {...data} />);
      res.status(statusCode);
      res.send(`<!doctype html>${html}`);
    }

  } catch (err) {
    console.log(err);
    next(err);
  } finally {
    removeHistoryListener();
  }
});

//
// Error handling
// -----------------------------------------------------------------------------
const pe = new PrettyError();
pe.skipNodeFiles();
pe.skipPackage('express');

app.use((err, req, res, next) => { // eslint-disable-line no-unused-vars
  console.log(pe.render(err)); // eslint-disable-line no-console
  const statusCode = err.status || 500;
  const html = ReactDOM.renderToStaticMarkup(
    <Html
      title="Internal Server Error"
      description={err.message}
      style={errorPageStyle._getCss()} // eslint-disable-line no-underscore-dangle
    >
      {ReactDOM.renderToString(<ErrorPage error={err} />)}
    </Html>
  );
  res.status(statusCode);
  res.send(`<!doctype html>${html}`);
});

//
// Launch the server
// -----------------------------------------------------------------------------
/* eslint-disable no-console */
// models.sync().catch(err => console.error(err.stack)).then(() => {
  app.listen(port, () => {
    console.log(`The server is running at http://localhost:${port}/`);
  });
// });
/* eslint-enable no-console */
