pragma solidity ^0.8.0;

interface IERC20 {
  function allowance(address owner, address spender) external view returns (uint256 remaining);
  function approve(address spender, uint256 value) external returns (bool success);
  function balanceOf(address owner) external view returns (uint256 balance);
  function decimals() external view returns (uint8 decimalPlaces);
  function decreaseApproval(address spender, uint256 addedValue) external returns (bool success);
  function increaseApproval(address spender, uint256 subtractedValue) external;
  function name() external view returns (string memory tokenName);
  function symbol() external view returns (string memory tokenSymbol);
  function totalSupply() external view returns (uint256 totalTokensIssued);
  function transfer(address to, uint256 value) external returns (bool success);
  function transferFrom(address from, address to, uint256 value) external returns (bool success);
}

contract Swap {
    address USDC;
    address USDT;
    address MyToken;
    mapping(address => uint256) private addressToSwappedAmount;
    constructor(address _usdc,address _usdt,address myToken){
        USDC = _usdc;
        USDT = _usdt;
        MyToken = myToken;
    }

    function swap(address token,uint256 amount) public{
        require(amount > 0,"Amount is zero");
        require(token == USDC || token == USDT,"Token not supported");
        IERC20 tokenA = IERC20(USDC);
        IERC20 tokenB = IERC20(USDT);
        if(token == USDC){
            require(tokenA.allowance(msg.sender,address(this)) >= amount,"Approval is required");
            _safeTransferFrom(tokenA,msg.sender,address(this),amount);
            tokenB.approve(address(this),amount);
            _safeTransferFrom(tokenB,address(this),msg.sender,amount);
        }else{
            require(tokenB.allowance(msg.sender,address(this)) >= amount,"Approval is required");
            _safeTransferFrom(tokenB,msg.sender,address(this),amount);
            tokenA.approve(address(this),amount);
            _safeTransferFrom(tokenA,address(this),msg.sender,amount);
        }
        addressToSwappedAmount[msg.sender] += amount;
        if(addressToSwappedAmount[msg.sender] >= 200){
                _reward(msg.sender);
        }

    }

    function _safeTransferFrom(IERC20 token ,address sender, address receiver, uint256 amount) internal{
        bool send = token.transferFrom(sender,receiver,amount);
        require(send,"Transfer Failed");
    }

    function _reward(address winner) internal{
        IERC20 rewardToken = IERC20(MyToken);
        bool send = rewardToken.transfer(winner,50);
        require(send,"Transfer Failed");
    }
}
