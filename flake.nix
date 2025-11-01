
{
    description = "An Anki add-on that fixes dark mode detection so that it happens immediately.";

    inputs.nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";

    outputs = { nixpkgs, ... }:
    let
        system = "x86_64-linux";
        pkgs = import nixpkgs { inherit system; };
        package = { anki-utils, nix-update-script, pygobject3 }: anki-utils.buildAnkiAddon rec {
            pname = "ankidarkmodefix";
            version = "1.0";
            src = pkgs.lib.fileset.toSource {
                root = ./.;
                fileset = pkgs.lib.fileset.unions [
                    ./__init__.py
                    ./vendor
                ];
            };
            passthru.updateSript = nix-update-script { };
            buildInputs = [ pygobject3 ];
            postInstall = ''
                # The path to the file we need to modify
                target_file="$out/$installPrefix/__init__.py"

                # The Python code we want to inject.
                # It adds a list of paths to the beginning of sys.path.
                injection_code="import sys; sys.path = [p for p in '${pkgs.python3.pkgs.makePythonPath buildInputs}'.split(':') if p] + sys.path"

                # Use sed to replace our placeholder with the real code.
                # The '@' symbols are used as delimiters for sed to avoid conflicts with '/' in paths.
                sed -i "s@# @NIX_PYTHON_PATH_INJECTION@@$injection_code@" "$target_file"
            '';
        };
    in
    {
        devShells."${system}".default = pkgs.mkShell {
            packages = with pkgs; [
                python313
                python313Packages.pip
                python313Packages.pygobject3
            ];
        };

        packages."${system}".default = pkgs.callPackage package { pygobject3 = pkgs.python313Packages.pygobject3; };
    };
}

