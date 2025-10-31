
{ pkgs ? import <nixpkgs> {} }:

(pkgs.buildFHSUserEnv {
  targetPkgs = pkgs: (with pkgs; [
    python314
    python314Packages.pip
  ]);
}).env

