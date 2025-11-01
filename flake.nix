
{
    description = "An Anki add-on that fixes dark mode detection so that it happens immediately.";

    inputs.nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";

    outputs = { nixpkgs, ... }:
    let
        system = "x86_64-linux";
        pkgs = import nixpkgs { inherit system; };
        package = { anki-utils, nix-update-script, pygobject3 }: anki-utils.buildAnkiAddon {
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

