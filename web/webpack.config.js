const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const webpack = require("webpack");
const Dotenv = require("dotenv-webpack");

// Dotenv.config();

module.exports = {
  mode: "development", // 'production'
  entry: "./src/index.jsx",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "bundle.js",
    publicPath: "/",
  },
  devServer: {
    allowedHosts: "all",
    historyApiFallback: {
      index: "/",
    }, // Redirige toutes les requêtes 404 vers index.html
    static: path.join(__dirname, "dist"),
    compress: true,
    port: 3000,
  },
  resolve: {
    extensions: [".js", ".jsx"],
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: "babel-loader",
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: "asset/resource",
        generator: {
          filename: "assets/images/[hash][ext][query]",
        },
      },
      {
        test: /\.css$/,
        use: [
          "style-loader", // Adds CSS to the DOM by injecting a <style> tag
          "css-loader", // Interprets @import and url() like import/require() and will resolve them
          "postcss-loader", // Processes CSS with PostCSS
        ],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "./public/index.html",
      favicon: "./public/favicon.ico",
    }),
    new webpack.DefinePlugin({
      "process.env.REACT_APP_API_PATH": JSON.stringify(
        process.env.REACT_APP_API_PATH
      ),
      "process.env.REACT_APP_API_WASABI_ENDPOINT": JSON.stringify(
        process.env.REACT_APP_API_WASABI_ENDPOINT
      ),
      "process.env.REACT_APP_API_WASABI_ACCESS_KEY": JSON.stringify(
        process.env.REACT_APP_API_WASABI_ACCESS_KEY
      ),
      "process.env.REACT_APP_API_WASABI_SECRET_KEY": JSON.stringify(
        process.env.REACT_APP_API_WASABI_SECRET_KEY
      ),
      "process.env.REACT_APP_API_WASABI_BUCKET_NAME": JSON.stringify(
        process.env.REACT_APP_API_WASABI_BUCKET_NAME
      ),
    }),
  ],
};
