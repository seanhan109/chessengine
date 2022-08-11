using System;
using System.Collections;
using System.Collections.generic;
using UnityEngine;

public class BoardManager : MonoBehaviour
{
    private void DrawChessBoard()
    {
        Vector3 widthline = Vector3.right * 8;
        Vector3 heightline = Vector3.forward * 8;

        for (int i = 0; i <= 8; ++i)
        {
            Vector3 start = Vector3.forward * i;
            Debug.DrawLine(start, start + widthline);
            for (int j = 0; j <= 8; ++j)
            {
                start = Vector3.right * j;
                Debug.DrawLine(start, start + heightline);
            }
        }

        if (selectionX >= 0 && selectionY >= 0)
        {
            Debug.DrawLine(Vector3.forward * selectionY + Vector3.right * selectionX,
                Vector3.forward * (selectionY + 1) + Vector3.right * (selectionX + 1));
            Debug.DrawLine(Vector3.forward * selectionY + Vector3.right * (selectionX + 1),
                Vector3.forward * (selectionY + 1) + Vector3.right * selectionX);
        }
    }

    private void UpdateSelection()
    {
        if (!Camera.main) return;

        RaycastHit hit;
        float raycastDistance = 25.0f;
        if (Physics.Raycast(Camera.main.ScreenPointToRay(Input.mousePosition), out hit, raycastDistance, LayerMask.GetMask("Chess Plane")))
        {
            selectionX = (int)hit.point.x;
            selectionY = (int)hit.point.z;
        }
        else
        {
            selectionX = -1;
            selectionY = -1;
        }
    } 
}

public abstract class ChessFigure : MonoBehaviour
{
    public int CurrentX{get; set;}
    public int CurrentY{get; set;}
    public bool isWhite;

    public void SetPosition(int x, int y)
    {
        CurrentX = x;
        CurrentY = y;
    }

    public virtual bool[,] PossibleMove()
    {
        return new bool[8,8];
    }
}