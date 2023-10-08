// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";{% if burnable %}
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";{% endif %}{% if pausable %}
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol";{% endif %}
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";

contract MyToken is 
    ERC20, {% if burnable %}ERC20Burnable, {% endif %}{% if pausable %}ERC20Pausable, {% endif %}Ownable, ERC20Permit {
    constructor()
        ERC20("{{ name }}", "{{ symbol }}")
        Ownable({{ owner }})
        ERC20Permit("{{ name }}")
    {
        {% if mintable %}_mint(msg.sender, {{ premint }} * 10 ** decimals());
        {% endif %}//transferOwnership({{ owner }});
    }
    {% if pausable %}

    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }
    {% endif %}{% if mintable %}

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }
    {% endif %}{% if pausable %}

    // The following functions are overrides required by Solidity.

    function _update(address from, address to, uint256 value)
        internal
        override(ERC20, ERC20Pausable)
    {
        super._update(from, to, value);
    }
    {% endif %}
}
